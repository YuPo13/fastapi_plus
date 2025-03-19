# fastapi_plus

## Overview
This project is a **FastAPI-based REST API** that allows users to manage authors and books using an **SQLite database**. It provides endpoints to **create, retrieve, and delete** authors and books.

## Features
- **Create an Author** (POST `/authors/`)
- **Retrieve Authors** (GET `/authors/`)
- **Delete an Author by ID** (DELETE `/authors/{author_id}`)
- **Create a Book** (POST `/books/`)
- **Retrieve Books** (GET `/books/`)

## Installation

### Prerequisites
Ensure you have **Python 3.11** installed.

### 1. Clone the Repository
```sh
 git clone https://github.com/YuPo13/fastapi_plus
 cd fastapi_plus
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

## Running the Application
Start the FastAPI server using **Uvicorn**:
```sh
uvicorn main:app --reload
```

By default, the server runs at: **http://127.0.0.1:8000**

## API Endpoints

### 📌 **Authors**
- **Add an Author**
  ```http
  POST /authors/
  ```
  **Request Body:**
  ```json
  {
    "name": "Joan",
    "surname": "Rowling",
    "country": "United Kingdom"
  }
  ```

- **Get All Authors**
  ```http
  GET /authors/
  ```

- **Delete an Author by ID**
  ```http
  DELETE /authors/{author_id}
  ```

### 📌 **Books**
- **Add a Book**
  ```http
  POST /books/
  ```
  **Request Body:**
  ```json
  {
    "title": "Harry Potter and the Sorcerer's Stone",
    "author_id": 1,
    "published_year": 1997
  }
  ```

- **Get All Books**
  ```http
  GET /books/
  ```

## Testing with Postman
1. Open **Postman**
2. Choose the request type (GET, POST, DELETE, etc.)
3. Enter the appropriate endpoint URL
4. If required, go to **Body** → Select **raw** → Choose **JSON**
5. Enter the request payload and click **Send**

## Database Migrations
We use **Alembic** for database migrations.

### **1. Initialize Alembic**
```sh
alembic init alembic
```

### **2. Configure `alembic.ini`**
Edit `alembic.ini` and set:
```
sqlalchemy.url = sqlite:///./library.db
```

### **3. Generate and Apply Migrations**
```sh
alembic revision --autogenerate -m "Added new columns"
alembic upgrade head
```
