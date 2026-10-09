# Endpoint inventory — FakeStoreAPI old-version-production

Source type: openapi3 · Servers: https://fakestoreapi.com · Endpoints: 16

`*` = required. Body/response names are schema names from the spec.

| # | Method | Path | Summary | Tags | Auth | Path params | Query params | Body | Responses |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GET | `/products` | Get all products | Products | unspecified |  |  |  | 200:Product[], 400:Bad request |
| 2 | POST | `/products` | Add a new product | Products | unspecified |  |  | Product ((required) id:integer, title:string, price:number, description:string, category:string, image:string) | 201:Product, 400:Bad request |
| 3 | GET | `/products/{id}` | Get a single product | Products | unspecified | id* |  |  | 200:Product, 400:Bad request |
| 4 | PUT | `/products/{id}` | Update a product | Products | unspecified | id* |  | Product ((required) id:integer, title:string, price:number, description:string, category:string, image:string) | 200:Product, 400:Bad request |
| 5 | DELETE | `/products/{id}` | Delete a product | Products | unspecified | id* |  |  | 200:Product deleted successfully, 400:Bad request |
| 6 | GET | `/carts` | Get all carts | Carts | unspecified |  |  |  | 200:Cart[], 400:Bad request |
| 7 | POST | `/carts` | Add a new cart | Carts | unspecified |  |  | Cart ((required) id:integer, userId:integer, products:array) | 201:Cart, 400:Bad request |
| 8 | GET | `/carts/{id}` | Get a single cart | Carts | unspecified | id* |  |  | 200:Cart, 400:Bad request |
| 9 | PUT | `/carts/{id}` | Update a cart | Carts | unspecified | id* |  | Cart ((required) id:integer, userId:integer, products:array) | 200:Cart, 400:Bad request |
| 10 | DELETE | `/carts/{id}` | Delete a cart | Carts | unspecified | id* |  |  | 200:Cart deleted successfully, 400:Bad request |
| 11 | GET | `/users` | Get all users | Users | unspecified |  |  |  | 200:User[], 400:Bad request |
| 12 | POST | `/users` | Add a new user | Users | unspecified |  |  | User ((required) id:integer, username:string, email:string, password:string) | 201:User, 400:Bad request |
| 13 | GET | `/users/{id}` | Get a single user | Users | unspecified | id* |  |  | 200:User, 400:Bad request |
| 14 | PUT | `/users/{id}` | Update a user | Users | unspecified | id* |  | User ((required) id:integer, username:string, email:string, password:string) | 200:User, 400:Bad request |
| 15 | DELETE | `/users/{id}` | Delete a user | Users | unspecified | id* |  |  | 200:User deleted successfully, 400:Bad request |
| 16 | POST | `/auth/login` | Login | Auth | unspecified |  |  | Login ((required) username:string, password:string) | 200:LoginResponse, 400:Bad request |
