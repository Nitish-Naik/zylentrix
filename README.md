# RESTful API for User Management

This project implements a RESTful API for user management with basic CRUD (Create, Read, Update, Delete) operations. The API allows users to create, read, update, and delete user records.

## Technologies Used

- **Python** 3.8+
- **Flask** (Web framework)
- **SQLite** (Lightweight database)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
   ```sh
   [git clone (https://github.com/Nitish-Naik/zylentrix.git)
   cd zylentrix
   ```

2. Create and activate a virtual environment (recommended):
   ```sh
   python -m venv venv
   ```
   - For Windows:
     ```sh
     venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

3. Install the required packages:
   ```sh
   pip install flask
   ```

### Run the Application

```sh
python app.py
```

The API will be available at: `http://127.0.0.1:5000`

---

## API Endpoints

### 1. Create a User
- **URL:** `/api/users`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }
  ```
- **Success Response:**
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "message": "User created successfully"
  }
  ```
- **Error Responses:**
  - `400 Bad Request` (Invalid input)
  - `409 Conflict` (Email already exists)
  - `500 Internal Server Error`

### 2. Retrieve All Users
- **URL:** `/api/users`
- **Method:** `GET`
- **Success Response:**
  ```json
  {
    "users": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
      },
      {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 25
      }
    ]
  }
  ```
- **Error Response:** `500 Internal Server Error`

### 3. Retrieve a Single User
- **URL:** `/api/users/<user_id>`
- **Method:** `GET`
- **Success Response:**
  ```json
  {
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "age": 30
    }
  }
  ```
- **Error Responses:**
  - `404 Not Found` (User does not exist)
  - `500 Internal Server Error`

### 4. Update a User
- **URL:** `/api/users/<user_id>`
- **Method:** `PUT`
- **Request Body:**
  ```json
  {
    "name": "John Doe Updated",
    "email": "john.updated@example.com",
    "age": 31
  }
  ```
- **Success Response:**
  ```json
  {
    "user": {
      "id": 1,
      "name": "John Doe Updated",
      "email": "john.updated@example.com",
      "age": 31
    },
    "message": "User updated successfully"
  }
  ```
- **Error Responses:**
  - `400 Bad Request` (Invalid input)
  - `404 Not Found` (User does not exist)
  - `409 Conflict` (Email already exists)
  - `500 Internal Server Error`

### 5. Delete a User
- **URL:** `/api/users/<user_id>`
- **Method:** `DELETE`
- **Success Response:**
  ```json
  {
    "message": "User deleted successfully"
  }
  ```
- **Error Responses:**
  - `404 Not Found` (User does not exist)
  - `500 Internal Server Error`

---

## Sample API Usage

### Create a User
```sh
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john.doe@example.com", "age": 30}'
```

### Get All Users
```sh
curl -X GET http://127.0.0.1:5000/api/users
```

### Get a Single User
```sh
curl -X GET http://127.0.0.1:5000/api/users/1
```

### Update a User
```sh
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe Updated", "email": "john.updated@example.com", "age": 31}'
```

### Delete a User
```sh
curl -X DELETE http://127.0.0.1:5000/api/users/1
```

---

## Security Considerations

- **Input Validation:** The API validates all user inputs before processing.
- **Error Handling:** Proper error messages are provided without exposing sensitive information.
- **Database Security:** Uses parameterized queries to prevent SQL injection attacks.
- **Email Uniqueness:** Ensures emails are unique to prevent duplicate records.


---

## License

This project is licensed under the MIT License.

