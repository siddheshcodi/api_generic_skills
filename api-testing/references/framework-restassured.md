# Framework: Java + REST Assured + JUnit 5

Good fit for Java/Spring teams and existing Maven/Gradle QA projects.
If the project already has API tests, follow their existing structure instead of this layout.

## Dependencies (Maven `pom.xml`, test scope)
```xml
<dependencies>
  <dependency><groupId>io.rest-assured</groupId><artifactId>rest-assured</artifactId><version>5.4.0</version><scope>test</scope></dependency>
  <dependency><groupId>io.rest-assured</groupId><artifactId>json-schema-validator</artifactId><version>5.4.0</version><scope>test</scope></dependency>
  <dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter</artifactId><version>5.10.2</version><scope>test</scope></dependency>
  <dependency><groupId>org.yaml</groupId><artifactId>snakeyaml</artifactId><version>2.2</version><scope>test</scope></dependency>
  <dependency><groupId>org.hamcrest</groupId><artifactId>hamcrest</artifactId><version>2.2</version><scope>test</scope></dependency>
</dependencies>
<!-- maven-surefire-plugin 3.x writes JUnit XML to target/surefire-reports automatically -->
```
Use the latest stable versions available to the project; the ones above are known-good.

## Layout
```
src/test/java/api/
├── support/
│   ├── TestConfig.java     # reads api-test.config.yaml + env vars
│   ├── Auth.java           # builds auth header from config
│   └── BaseApiTest.java    # RequestSpecification, helpers, cleanup
├── users/                  # one package per module
│   ├── ListUsersApiTest.java      # one class per operation, positive + negative together
│   ├── GetUserApiTest.java
│   ├── CreateUserApiTest.java
│   ├── UpdateUserApiTest.java
│   └── DeleteUserApiTest.java
├── orders/ ...
└── integration/            # cross-module flows
    └── OrderFlowApiTest.java
src/test/resources/schemas/user.json
```
Every test has `@Tag("positive")` or `@Tag("negative")` plus `smoke`/`regression`; each class has a
module tag (`@Tag("users")`, `@Tag("integration")`). Select with `-Dgroups`, never split classes by
test type.
```
```

## TestConfig.java
```java
package api.support;

import org.yaml.snakeyaml.Yaml;
import java.io.FileInputStream;
import java.util.Map;

@SuppressWarnings("unchecked")
public final class TestConfig {
    public static final Map<String, Object> CONFIG;
    public static final Map<String, Object> ENV;

    static {
        try (var in = new FileInputStream("api-test.config.yaml")) {
            CONFIG = new Yaml().load(in);
        } catch (Exception e) {
            throw new IllegalStateException("Cannot read api-test.config.yaml", e);
        }
        var envs = (Map<String, Object>) CONFIG.get("environments");
        String name = System.getenv().getOrDefault("API_ENV", (String) envs.get("default"));
        ENV = (Map<String, Object>) envs.get(name);
    }

    public static Map<String, Object> section(String key) {
        return (Map<String, Object>) CONFIG.getOrDefault(key, Map.of());
    }

    public static String env(String name) {
        String v = System.getenv(name);
        if (v == null || v.isBlank()) throw new IllegalStateException("Env var " + name + " is not set");
        return v;
    }

    public static boolean destructiveAllowed() {
        boolean prod = Boolean.TRUE.equals(ENV.get("is_production"));
        return !prod || Boolean.TRUE.equals(section("testing").get("allow_destructive_on_production"));
    }
}
```

## Auth.java
```java
package api.support;

import io.restassured.RestAssured;
import java.util.Base64;
import java.util.Map;
import static api.support.TestConfig.*;

@SuppressWarnings("unchecked")
public final class Auth {
    /** Returns {headerName, headerValue} or null for no auth. */
    public static String[] header() {
        var auth = section("auth");
        String type = (String) auth.getOrDefault("type", "none");
        switch (type) {
            case "none": return null;
            case "bearer": {
                var b = (Map<String, Object>) auth.get("bearer");
                return new String[]{"Authorization", "Bearer " + env((String) b.get("token_env"))};
            }
            case "basic": {
                var b = (Map<String, Object>) auth.get("basic");
                String raw = env((String) b.get("username_env")) + ":" + env((String) b.get("password_env"));
                return new String[]{"Authorization", "Basic " + Base64.getEncoder().encodeToString(raw.getBytes())};
            }
            case "api_key": {
                var k = (Map<String, Object>) auth.get("api_key");
                return new String[]{(String) k.get("header"), env((String) k.get("value_env"))};
            }
            case "oauth2_client_credentials": {
                var o = (Map<String, Object>) auth.get("oauth2_client_credentials");
                String token = RestAssured.given()
                    .formParam("grant_type", "client_credentials")
                    .formParam("client_id", env((String) o.get("client_id_env")))
                    .formParam("client_secret", env((String) o.get("client_secret_env")))
                    .formParam("scope", o.getOrDefault("scope", ""))
                    .post((String) o.get("token_url"))
                    .then().statusCode(200).extract().path("access_token");
                return new String[]{"Authorization", "Bearer " + token};
            }
            case "login_endpoint": {
                var l = (Map<String, Object>) auth.get("login_endpoint");
                String body = ((String) l.get("body_template"))
                    .replace("{username}", env((String) l.get("username_env")))
                    .replace("{password}", env((String) l.get("password_env")));
                String token = RestAssured.given().baseUri((String) ENV.get("base_url"))
                    .contentType("application/json").body(body)
                    .request((String) l.getOrDefault("method", "POST"), (String) l.get("path"))
                    .then().statusCode(200).extract().path((String) l.get("token_json_path"));
                return new String[]{(String) l.getOrDefault("header", "Authorization"),
                                    l.getOrDefault("prefix", "Bearer ") + token};
            }
            default: throw new IllegalStateException("Unknown auth type: " + type);
        }
    }
}
```

## BaseApiTest.java
```java
package api.support;

import io.restassured.builder.RequestSpecBuilder;
import io.restassured.specification.RequestSpecification;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import java.util.*;
import static io.restassured.RestAssured.given;
import static api.support.TestConfig.*;

@SuppressWarnings("unchecked")
public abstract class BaseApiTest {
    protected static RequestSpecification api;      // authenticated
    protected static RequestSpecification anonApi;  // no auth
    private final Deque<String> cleanup = new ArrayDeque<>();

    @BeforeAll
    static void setUpSpecs() {
        var headers = (Map<String, String>) section("defaults").getOrDefault("default_headers", Map.of());
        var anon = new RequestSpecBuilder().setBaseUri((String) ENV.get("base_url"))
            .addHeaders(headers).setContentType("application/json");
        anonApi = anon.build();
        var authed = new RequestSpecBuilder().addRequestSpecification(anonApi);
        String[] h = Auth.header();
        if (h != null) authed.addHeader(h[0], h[1]);
        api = authed.build();
    }

    protected String unique() {
        String prefix = (String) section("testing").getOrDefault("test_data_prefix", "qa_auto_");
        return prefix + UUID.randomUUID().toString().substring(0, 8);
    }

    protected void deleteAfter(String path) { cleanup.push(path); }

    @AfterEach
    void cleanUp() {
        if (Boolean.FALSE.equals(section("testing").get("cleanup_test_data"))) return;
        while (!cleanup.isEmpty()) given().spec(api).delete(cleanup.pop());
    }
}
```

## Example tests (`users/CreateUserApiTest.java`, condensed) — ID in every display name, type tag on every test
```java
package api.users;

import api.support.BaseApiTest;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import java.util.HashMap;
import java.util.Map;
import static io.restassured.RestAssured.given;
import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;
import static org.junit.jupiter.api.Assumptions.assumeTrue;
import static api.support.TestConfig.destructiveAllowed;

@Tag("users")
class CreateUserApiTest extends BaseApiTest {

    @Test @Tag("smoke") @Tag("positive")
    @DisplayName("API-USERS-001 create user with required fields")
    void createUser() {
        assumeTrue(destructiveAllowed(), "destructive test skipped on production");
        String email = unique() + "@example.com";
        String id = given().spec(api).body(Map.of("name", unique(), "email", email))
            .when().post("/users")
            .then().statusCode(201)
            .body("email", equalTo(email))
            .body(matchesJsonSchemaInClasspath("schemas/user.json"))
            .extract().path("id").toString();
        deleteAfter("/users/" + id);
    }

    @ParameterizedTest(name = "API-USERS-004 create user without {0} is rejected")
    @Tag("regression") @Tag("negative")
    @ValueSource(strings = {"name", "email"})
    void createUserMissingField(String missing) {
        assumeTrue(destructiveAllowed(), "destructive test skipped on production");
        Map<String, Object> body = new HashMap<>(Map.of("name", unique(), "email", unique() + "@example.com"));
        body.remove(missing);
        given().spec(api).body(body).when().post("/users")
            .then().statusCode(anyOf(is(400), is(422)));
    }

    @Test @Tag("smoke") @Tag("negative")   // lives in ListUsersApiTest in a real suite
    @DisplayName("API-USERS-010 get users without token returns 401")
    void noToken() {
        given().spec(anonApi).when().get("/users").then().statusCode(401);
    }
}
```
Add `junit-jupiter-params` if your JUnit artifact doesn't include it. Add
`.log().ifValidationFails()` to specs while debugging — it prints request/response only on failure.

## Run commands
```bash
mvn test -Dgroups=smoke                    # smoke
mvn test                                   # full
API_ENV=staging mvn test -Dgroups=smoke    # other env
mvn test -Dtest=CreateUserApiTest#noToken  # rerun one case
mvn test -Dgroups=negative                 # all negative tests
mvn test -Dgroups="users & negative"       # one module, one type (JUnit 5 tag expression)
mvn test -Dgroups=integration              # cross-module flows
# Gradle: ./gradlew test --tests 'api.users.*'  (use useJUnitPlatform { includeTags 'smoke' })
```
JUnit XML: `target/surefire-reports/TEST-*.xml` (Gradle: `build/test-results/test/*.xml`).
Then: `python <skill>/scripts/parse_results.py target/surefire-reports/*.xml --out api-test-reports/results`
