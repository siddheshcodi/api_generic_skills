# Framework: TypeScript + Playwright (API testing via `request`)

Good fit when the team already uses JS/TS or Playwright for UI tests (one tool for both).
If the project already has API tests, follow their existing structure instead of this layout.

## Dependencies
```bash
npm i -D @playwright/test ajv ajv-formats yaml
# No browsers needed for API-only tests.
```

## Layout
```
tests/api/
├── config.ts              # reads api-test.config.yaml + env vars
├── auth.ts                # builds auth headers from config
├── fixtures.ts            # api / anonApi / unique / cleanup fixtures
├── schema.ts              # Ajv schema assertion helper
├── schemas/user.json
├── users/                         # one folder per module
│   ├── list-users.spec.ts         # one file per operation, positive + negative together
│   ├── get-user.spec.ts
│   ├── create-user.spec.ts
│   ├── update-user.spec.ts
│   └── delete-user.spec.ts
├── orders/ ...
└── integration/                   # cross-module flows
    └── order-flow.spec.ts
playwright.config.ts
```
Every test title carries the ID and tags: `@smoke`/`@regression`, `@positive`/`@negative`, and the
module (`@users`, `@integration`) — select slices with `--grep`, never split files by test type.

## playwright.config.ts
```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/api',
  timeout: 60_000,
  reporter: [
    ['list'],
    ['junit', { outputFile: 'api-test-reports/junit.xml' }],
    ['html', { outputFolder: 'api-test-reports/html', open: 'never' }],
  ],
});
```

## config.ts
```ts
import fs from 'fs';
import path from 'path';
import YAML from 'yaml';

export const CONFIG = YAML.parse(
  fs.readFileSync(path.resolve(__dirname, '../../api-test.config.yaml'), 'utf8'),
);
export const ENV_NAME = process.env.API_ENV ?? CONFIG.environments.default;
export const ENV = CONFIG.environments[ENV_NAME];

export function env(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Environment variable ${name} is not set`);
  return v;
}
```

## auth.ts
```ts
import { request } from '@playwright/test';
import { CONFIG, ENV, env } from './config';

export async function authHeaders(): Promise<Record<string, string>> {
  const a = CONFIG.auth ?? { type: 'none' };
  switch (a.type) {
    case 'none': return {};
    case 'bearer': return { Authorization: `Bearer ${env(a.bearer.token_env)}` };
    case 'basic': {
      const raw = `${env(a.basic.username_env)}:${env(a.basic.password_env)}`;
      return { Authorization: `Basic ${Buffer.from(raw).toString('base64')}` };
    }
    case 'api_key': return { [a.api_key.header]: env(a.api_key.value_env) };
    case 'oauth2_client_credentials': {
      const o = a.oauth2_client_credentials;
      const ctx = await request.newContext();
      const r = await ctx.post(o.token_url, { form: {
        grant_type: 'client_credentials',
        client_id: env(o.client_id_env),
        client_secret: env(o.client_secret_env),
        scope: o.scope ?? '',
      }});
      if (!r.ok()) throw new Error(`Token request failed: ${r.status()}`);
      return { Authorization: `Bearer ${(await r.json()).access_token}` };
    }
    case 'login_endpoint': {
      const l = a.login_endpoint;
      const body = JSON.parse(l.body_template
        .replace('{username}', env(l.username_env))
        .replace('{password}', env(l.password_env)));
      const ctx = await request.newContext({ baseURL: ENV.base_url });
      const r = await ctx.fetch(l.path, { method: l.method ?? 'POST', data: body });
      if (!r.ok()) throw new Error(`Login failed: ${r.status()}`);
      let token: any = await r.json();
      for (const part of l.token_json_path.split('.')) token = token[part];
      return { [l.header ?? 'Authorization']: `${l.prefix ?? 'Bearer '}${token}` };
    }
    default: throw new Error(`Unknown auth type: ${a.type}`);
  }
}
```

## fixtures.ts
```ts
import { test as base, request, APIRequestContext } from '@playwright/test';
import { randomUUID } from 'crypto';
import { CONFIG, ENV } from './config';
import { authHeaders } from './auth';

const defaults = CONFIG.defaults?.default_headers ?? {};
const prefix = CONFIG.testing?.test_data_prefix ?? 'qa_auto_';
export const isProduction = !!ENV.is_production;
export const allowDestructive =
  !isProduction || !!CONFIG.testing?.allow_destructive_on_production;

type Fixtures = {
  api: APIRequestContext;
  anonApi: APIRequestContext;
  unique: () => string;
  cleanup: string[];
};

export const test = base.extend<Fixtures>({
  api: async ({}, use) => {
    const ctx = await request.newContext({
      baseURL: ENV.base_url,
      extraHTTPHeaders: { ...defaults, ...(await authHeaders()) },
    });
    await use(ctx);
    await ctx.dispose();
  },
  anonApi: async ({}, use) => {
    const ctx = await request.newContext({ baseURL: ENV.base_url, extraHTTPHeaders: defaults });
    await use(ctx);
    await ctx.dispose();
  },
  unique: async ({}, use) => use(() => `${prefix}${randomUUID().slice(0, 8)}`),
  cleanup: async ({ api }, use) => {
    const paths: string[] = [];
    await use(paths);
    if (CONFIG.testing?.cleanup_test_data !== false) {
      for (const p of paths.reverse()) await api.delete(p);
    }
  },
});
export { expect } from '@playwright/test';
```
Note: Playwright `baseURL` joins paths like a browser — use paths starting with `/` and a base URL
**without** a trailing path segment, or include the API prefix in every path (`/v1/users`).

## schema.ts
```ts
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import fs from 'fs';
import path from 'path';
import { expect } from '@playwright/test';

const ajv = new Ajv({ allErrors: true, strict: false });
addFormats(ajv);

export function expectSchema(body: unknown, name: string) {
  const schema = JSON.parse(fs.readFileSync(path.join(__dirname, 'schemas', `${name}.json`), 'utf8'));
  const valid = ajv.validate(schema, body);
  expect(valid, ajv.errorsText()).toBe(true);
}
```

## Example tests (`users.spec.ts`) — ID and tag in every title
```ts
import { test, expect, allowDestructive } from './fixtures';
import { expectSchema } from './schema';

test('API-USERS-001 create user with required fields @smoke @positive @users', async ({ api, unique, cleanup }) => {
  test.skip(!allowDestructive, 'destructive test skipped on production');
  const payload = { name: unique(), email: `${unique()}@example.com` };
  const r = await api.post('/users', { data: payload });
  expect(r.status(), await r.text()).toBe(201);
  const body = await r.json();
  cleanup.push(`/users/${body.id}`);
  expect(body.email).toBe(payload.email);
  expectSchema(body, 'user');
});

for (const missing of ['name', 'email']) {
  test(`API-USERS-004 create user without ${missing} is rejected @regression @negative @users`, async ({ api, unique }) => {
    test.skip(!allowDestructive, 'destructive test skipped on production');
    const payload: Record<string, string> = { name: unique(), email: `${unique()}@example.com` };
    delete payload[missing];
    const r = await api.post('/users', { data: payload });
    expect([400, 422], `got ${r.status()}: ${(await r.text()).slice(0, 300)}`).toContain(r.status());
  });
}

test('API-USERS-010 get users without token returns 401 @smoke @negative @users', async ({ anonApi }) => {
  expect((await anonApi.get('/users')).status()).toBe(401);
});
```

## Run commands
```bash
npx playwright test --grep @smoke                 # smoke
npx playwright test                               # full
API_ENV=staging npx playwright test --grep @smoke # other env
npx playwright test --grep "API-USERS-004"        # rerun one case
npx playwright test --grep @negative              # all negative tests
npx playwright test --grep "(?=.*@users)(?=.*@negative)"   # one module, one type
npx playwright test tests/api/integration         # cross-module flows
```
JUnit XML lands in `api-test-reports/junit.xml` (from the reporter config).
Then: `python <skill>/scripts/parse_results.py api-test-reports/junit.xml --out api-test-reports/results`
