# API Documentation

## Authentication

### JWT Authentication

The API uses JWT (JSON Web Token) for authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### Authentication Endpoints

#### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

Response:
```json
{
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "bearer"
}
```

#### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string"
}
```

Response:
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "created_at": "datetime"
}
```

#### Refresh Token

```http
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

Response:
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

## User Management

### Get Current User

```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

Response:
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Update User

```http
PUT /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
    "username": "string",
    "email": "string"
}
```

Response:
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "updated_at": "datetime"
}
```

## Error Responses

### 400 Bad Request

```json
{
    "error": "Bad Request",
    "message": "Invalid input data",
    "details": {
        "field": ["error message"]
    }
}
```

### 401 Unauthorized

```json
{
    "error": "Unauthorized",
    "message": "Invalid credentials"
}
```

### 403 Forbidden

```json
{
    "error": "Forbidden",
    "message": "Insufficient permissions"
}
```

### 404 Not Found

```json
{
    "error": "Not Found",
    "message": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
    "error": "Internal Server Error",
    "message": "An unexpected error occurred"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. The current limits are:

- 100 requests per minute for authenticated users
- 30 requests per minute for unauthenticated users

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1616721600
``` 