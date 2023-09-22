# Overview

This is a FastAPI-built API for a LUNCH APP that allows staff of an organization to share lunch with one another.

#TEAM NAME
EMPIRE

Detailed information about each **endpoints** can be found below.

## Table of Contents

- [Getting Started]
- [Endpoints]
    - [1. User Signup]
    - [2. User Login]
- [Request and Response Examples]
    

## Getting Started

For how to setup the application; check the README file here: https://github.com/hngx-org/Empire-food-backend/blob/staging/README.md

## Endpoints

The API provides the following endpoints for managing the persons resource:

### 1\. User Signup

- **Endpoint**: `POST /api/v1/user/signup`
- **Description**: This signs a new user up to the app.
- **Headers**: `Content-Type: application/json Accept: application/json`
- **Request Body**: JSON object with person information i.e `firstname`, `lastname` and `phonenumber`, `password`, `email`.
- **Response**: JSON object with a success message, status code of 201. Otherwise status code of 500 with "failed to create user" message.
    

### 2\. User Login

- **Endpoint**: `POST /api/v1/login`
- **Description**: This logs an existing user in to the app.
- **Headers**: `Content-Type: application/json Accept: application/json`
- **Request Body**: JSON object with person information i.e `email`, `password`.
- **Response**: JSON object with success message, status code of 201, access_token, refresh_token,email, id, is_admin. Otherwise status code of 403 with a "User authenticated successfully." message.
    

## Request and Response Examples

Here are some examples of how to use the API:

### 1\.  User Signup

- `POST /api/v1/user/signup  Content-Type: application/json`

```javascript
{  
    "firstname": "Komolafe",
    "lastname": "Dada",
    "phonenumber": phonenumber,
    "email": komo@gmail.com,
    "password": *****
}
```
- Responses: 

>Status code: 201

```javascript
{  
   "message": 'User registered successfully',
   "statusCode": 201,
   "data":    None
}
```

```
- Responses: 

>Status code: 500

```javascript
{  
  "statusCode": 500,
  "detail": "failed to create user"
}
```

### 2\. User Login

- `POST /api/v1/login`
- 
```javascript
{  
  "email": babadaju@gmail.com,
  "password": ****
}
```
- Responses:

>Status code: 201

```javascript
{
  "message": "User authenticated successfully.",
  "statusCode": 201,
  "data": {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": babadaju@gmail.com,
        "id": id,
        "is_admin": is_admin,
  }
}
```
>Status code: 403

```javascript
{
  "detail": "Invalid credentials.",
  "statusCode": 403,
}
```

##THANK YOU!!!
