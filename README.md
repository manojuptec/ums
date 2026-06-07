# ums
User Management System with Python

# FastAPI Authentication System

# Features

* User Registration
* User Login
* User Logout
* Token Authentication
* PostgreSQL Stored Functions
* FastAPI Swagger Documentation
* MVC Architecture
* Password Hashing
* PostgreSQL Database Integration
* Error Handling
* Response Validation

---

# Tech Stack

| Technology | Version |
| ---------- | ------- |
| Python     | 3.13+   |
| FastAPI    | Latest  |
| PostgreSQL | 15+     |
| pgAdmin    | Latest  |
| Uvicorn    | Latest  |
| Pydantic   | Latest  |
| Psycopg2   | Latest  |

---

# Project Structure

```text
project/

├── server.py
├── database/
│   └── connection.py
│
├── routers/
│   └── UserRoutes.py
│
├── controllers/
│   └── UserController.py
│
├── services/
│   └── UserService.py
│
├── schemas/
│   └── user_schema.py
│
├── db_script/
│   └── schema and all functions
│
```

---

# Python Installation

Download Python:

https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi
pip install uvicorn
pip install psycopg2-binary
pip install pydantic
pip install python-jose
pip install bcrypt
pip import psycopg2
import hashlib
```

# PostgreSQL Installation

Download PostgreSQL:

https://www.postgresql.org/download/

Install:

* PostgreSQL Server
* pgAdmin 4

Verify installation:

```sql
SELECT version();
```

---

# Create Database

```sql
CREATE DATABASE testing;
```

Connect database:

```sql
\c testing
```

---

# Create Users Table

```sql
-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    email character varying COLLATE pg_catalog."default",
    password character varying COLLATE pg_catalog."default",
    status smallint,
    added_date timestamp without time zone DEFAULT now(),
    updated_date timestamp without time zone DEFAULT now(),
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;
```

---

# Create User Token Table

```sql
-- Table: public.user_token

-- DROP TABLE IF EXISTS public.user_token;

CREATE TABLE IF NOT EXISTS public.user_token
(
    id integer NOT NULL DEFAULT nextval('user_token_id_seq'::regclass),
    user_id integer NOT NULL,
    token character varying COLLATE pg_catalog."default",
    user_device character varying COLLATE pg_catalog."default",
    ip character varying COLLATE pg_catalog."default",
    status smallint,
    added_date timestamp without time zone DEFAULT now(),
    updated_date timestamp without time zone DEFAULT now(),
    CONSTRAINT user_token_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_token
    OWNER to postgres;
```

---

# Create Register Function

```sql

/*
 select * from  public.user_aud(
null:: integer,
'a':: CHARACTER varying,
'a@gmail.com':: CHARACTER varying,
'123':: CHARACTER varying,
1:: smallint,
'add':: CHARACTER varying
)
*/

create or replace function public.user_aud(
_user_id integer,
_name CHARACTER varying,
_email CHARACTER varying,
_password CHARACTER varying,
_status smallint,
_action CHARACTER varying
)
returns json
LANGUAGE 'plpgsql'  
AS $BODY$

DECLARE 

BEGIN
     
	 if _action = 'add' then 
	 if (select count(1) from public.users where lower(email) = lower(_email)) > 0 then 
	 RAISE EXCEPTION 'User already exists, please login with your existing credentials';
	 end if;
   
	
    INSERT INTO public.users(name,email, password, status,added_date)
    VALUES (_name, lower(_email), _password, 1,now()
    ) returning id into _user_id;
                      
 	RETURN  json_build_object('user_id',_user_id,'message','User registered successfully!','status',1);
	 elseif _action = 'update' then 
	 if _user_id is null then 
	 RETURN  json_build_object('user_id',_user_id,'message','User id is required','status',0);
	 end if;
	 update public.users set 
	password = CASE when _password is null or _password = '' then password else _password end, 
	name = case when _name is null then name else _name end, 
	status = case when _status is null then status else _status end 
	where id = _user_id;
	RETURN  json_build_object('user_id',_user_id,'message','User details updated successfully!','status',1);
	 end if;
    
END;

$BODY$;
```

---

# Create Login Logout Function

```sql

/*
select * from  public.user_login_logout(
    null::integer,
	'a@gmail.com':: character varying,
	'123':: character varying,
	'asdrt':: character varying,
	null:: text[],
	'login'::character varying)
*/
CREATE OR REPLACE FUNCTION public.user_login_logout(
    _logged_user_id integer,
	_email character varying,
	_login_password character varying,
	_token character varying,
	_sessioninfo text[],
	_action character varying)
    returns json
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
	_user_id integer;
    _password character varying;
    _status smallint;
    _is_logged_in smallint;
	_roleID integer;
	_is_verified boolean;
	_name character varying;
	_added_date date;
    BEGIN
	if _action ='login' then 
      SELECT id, password, status,name,added_date into _user_id, _password, _status,_name,_added_date
      from public.users 
      where 
      	lower(email) = lower(_email);  
      
      if _user_id is null then
      	RAISE EXCEPTION 'Invalid login-id --> %', _email
					USING HINT = 'User does not exist';
      end if;
      
	 
      if _password <> _login_password then
      	RAISE EXCEPTION 'Invalid password';
      end if;
	 
	 
      -- Insert new entry for current device
	  INSERT INTO user_token (user_id, token) 
	  VALUES (_user_id, _token);
      	RETURN  json_build_object('id',_user_id, 'status',_status,'name',_name,'added_date',_added_date,'email',_email,'message','User logged in successfully!','status',1);  
     elseif _action = 'logout' then 
      if _logged_user_id is null  then 
	 RAISE EXCEPTION 'User id is required';
	 end if;
	 delete from user_token where user_id=_logged_user_id and token = _token;
	 RETURN  json_build_object('user_id',_logged_user_id,'message','User logged out successfully!','status',1);  
    end if;	 
    END;

$BODY$;

```
# Create User Detail Function

```sql

/*
select * from  public.get_user_details(
    9::integer)
	
*/
CREATE OR REPLACE FUNCTION public.get_user_details(
    _user_id integer)
    returns table(name character varying,email character varying,id integer,status smallint,added_date date)
    LANGUAGE 'plpgsql'
AS $BODY$

DECLARE
    BEGIN
	return query
	select u.name,u.email,u.id,u.status ,u.added_date::date from public.users u where u.id= _user_id;
    END;

$BODY$;


```
---

# Database Configuration

db.py

```python
import psycopg2

def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="auth_db",
        user="postgres",
        password="your_password",
        port="5432"
    )
```

---

# Run Application

```bash
uvicorn main:app --reload
```

Server:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Redoc:

```text
http://localhost:8000/redoc
```

---

# API Documentation

## Register User

Endpoint

```http
POST /api/register
```

Request

```json
{
  "name": "Manoj",
  "email": "manoj@gmail.com",
  "password": "Password123"
}
```

Response

```json
{
  "status": 201,
  "message": "User registered successfully"
}
```

---

## Login User

Endpoint

```http
POST /api/login
```

Request

```json
{
  "email": "manoj@gmail.com",
  "password": "Password123"
}
```

Response

```json
{
  "id": 1,
  "name": "Manoj",
  "email": "manoj@gmail.com",
  "token": "jwt_token_here",
  "status": 1
}
```

---

## Logout User

Endpoint

```http
POST /api/logout?user_id=1
```

Header

```http
token: jwt_token_here
```

Response

```json
{
  "status": 200,
  "message": "User logged out successfully"
}
```

---

## Get User By ID

Endpoint

```http
GET /api/user/{user_id}
```

Example

```http
GET /api/user/1
```

Response

```json
{
  "id": 1,
  "name": "Manoj",
  "email": "manoj@gmail.com",
  "status": 1,
  "added_date": "2026-06-04"
}
```

---

# Error Responses

## User Not Found

```json
{
  "status": 404,
  "error": "User does not exist"
}
```

## Invalid Password

```json
{
  "status": 401,
  "error": "Invalid password"
}
```

## Internal Server Error

```json
{
  "status": 500,
  "error": "Internal server error"
}
```

---

# Security Recommendations

* Store secrets in environment variables
* Use HTTPS in production
* Hash passwords before storing
* Validate all inputs
* Use database connection pooling

---

# Future Enhancements

* Refresh Token Support
* Role Based Access Control (RBAC)
* Email Verification
* Forgot Password
* Reset Password
* OAuth Login
* Docker Support
* CI/CD Pipeline

---

# Author

Manoj Kumar

Backend Architect | Python | FastAPI | PostgreSQL | Node.js

11+ Years Experience
