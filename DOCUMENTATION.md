# Overview

This is a FastAPI-built API for a LUNCH APP that allows staff of an organization to share lunch with one another. Detailed information about each **endpoints** can be found below.

# TEAM NAME
EMPIRE

## Table of Contents

- [Getting Started]
- [Endpoints]
    - [1. User Signup]
    - [2. User Login]
    - [3. Refresh Token]
    - [4. All Lunch]
    - [5. A Lunch]
    - [6. Register User in Organaization]
- [Request and Response Examples]
    

## Getting Started

For how to setup the application; check the README file here: https://github.com/hngx-org/Empire-food-backend/blob/staging/README.md

## Endpoints

The API provides the following endpoints:

### 1\. User Signup

- **Endpoint**: `POST /api/v1/user/signup`
- **Description**: This signs a new user up to the app.
- **Headers**: `Content-Type: application/json Accept: application/json`
- **Request Body**: JSON object with person information i.e `firstname`, `lastname` and `phonenumber`, `password`, `email`.
- **Response**: JSON object with a success message, status code of 201. Otherwise status code of 500 with "failed to create user" message.
    

### 2\. User Login

- **Endpoint**: `POST /api/v1/login`
- **Description**: This logs an existing user into the app.
- **Headers**: `Content-Type: application/json Accept: application/json`
- **Request Body**: JSON object with person information i.e `email`, `password`.
- **Response**: JSON object with a success message, status code of 201, access_token, refresh_token,email, id, is_admin. Otherwise status code of 403 with a "User authenticated successfully." message.

### 3\. Refresh Token

- **Endpoint**: `POST /api/v1/refresh/{id}`
- **Description**: This gives the user a new access token 
- **Headers**: `Content-Type: application/String Accept: application/String`
- **Request Body**: Refresh token which is a `string`.
- **Response**: JSON object with a success message, status code of 200 and new access_token.

### 4\. All Lunch

- **Endpoint**: `GET /api/v1/lunch/all`
- **Description**: This returns all the lunch 
- **Headers**: `Content-Type: application/string Accept: application/string`
- **Response**: JSON object with success message, status code of 200 and all received and sent lunches by the user.

### 5\. A Lunch

- **Endpoint**: `GET /api/v1/lunch/{id}`
- **Description**: This returns a specific lunch 
- **Headers**: `Content-Type: application/string Accept: application/string`
- **Response**: JSON object with success message, status code of 200 and all data about the lunch. Otherwise status code of 404 and error message of "lunch not found".

### 6\. Register User in Organization

- **Endpoint**: `GET /api/v1//organization/staff/signup`
- **Description**: This signs up a user for an organization
- **Headers**: `Content-Type: application/json Accept: application/json`
- **Response**: JSON object with success message, status code of 201, access token, email, id and isAdmin. Otherwise status codes of 406 (incorrect OTP) or  409 (User already exists)
    

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

>Status code: 500

```javascript
{  
  "statusCode": 500,
  "detail": "failed to create user"
}
```

### 2\. User Login

- `POST /api/v1/login`

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

### 3\. Refresh Token

- `POST /api/v1/refresh/{id}`

```javascript
refresh token: string
```
- Responses:

>Status code: 200

```javascript
{
  "message": "User authenticated successfully.",
  "statusCode": 200,
  "data": {
        "access_token": access_token,
  }
}
```

### 4\.All Lunch 

- `POST /api/v1/lunch/all`

- Responses:

>Status code: 200

```javascript
{
  "message": "Lunch retrieved successfully",
  "statusCode": 200,
  "data": [
		{
			"receiverId": 2,
			"senderId": 7,
            "quantity": 5,
			"redeemed": false,
            "note": "Special instructions for the lunch",
			"created_at": created date and time
            "id": 30
		},
		{
			"receiverId": 4,
			"senderId": 5,
		  "quantity": 5,
			"redeemed": false,
		  "note": "Special instructions for the lunch",
			"created_at": created date and time,
			"id": 20
		}
	]
}

```

### 5\.A Lunch 

- `POST /api/v1/lunch/{id}`

- Responses:

>Status code: 200

```javascript
{
  "data": {
		"receiverId": 2,
		"senderId": 6,
        "quantity": 5,
		"redeemed": false,
        "note": "Special instructions for the lunch",
		"created_at": created date and time,
		"id": id
	}
}
```
```
>Status code: 404

```javascript
{
  "detail": "Error: Lunch not found.",
  "statusCode": 404,
}
```

### 6\. Register User in Organization

- `GET /api/v1//organization/staff/signup`

- Responses:

>Status code: 201

```javascript
{
        'message': 'User registered successfully',
        'statusCode': 201,
        'data': {
            'access_token': access_tok,
            'email': email,
            'id': 5,
            'isAdmin': false
        }
}
```
>Status code: 406

```javascript
{
  "detail": "Incorrect OTP.",
  "statusCode": 406,
}
```
>Status code: 409

```javascript
{
  "detail": "User already exists.",
  "statusCode": 409,
}
```
## THANK YOU!!!
