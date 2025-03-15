# app.py
from flask import Flask, request, jsonify, abort
import sqlite3
from sqlite3 import Error
import os

app = Flask(__name__)

# Database setup
DB_NAME = "users.db"

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table():
    """Create users table if it doesn't exist"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL
                )
            ''')
            conn.commit()
        except Error as e:
            print(e)
        finally:
            print("Table created")
            conn.close()

# Initialize database
create_table()

# Helper function to validate user data
def validate_user_data(data):
    """Validate user data for creation and updates"""
    errors = []
    
    if not data.get('name'):
        errors.append("Name is required")
    
    if not data.get('email'):
        errors.append("Email is required")
    elif '@' not in data.get('email', ''):
        errors.append("Invalid email format")
    
    if 'age' not in data:
        errors.append("Age is required")
    elif not isinstance(data.get('age'), int) or data.get('age') < 0:
        errors.append("Age must be a positive integer")
    
    return errors

# API Endpoints
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    if not request.json:
        abort(400, description="Request must be JSON")
    
    data = request.json
    validation_errors = validate_user_data(data)
    
    if validation_errors:
        return jsonify({"error": "Validation failed", "details": validation_errors}), 400
    
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (data['name'], data['email'], data['age'])
            )
            conn.commit()
            
            # Get the ID of the newly created user
            user_id = cursor.lastrowid
            
            return jsonify({
                "id": user_id,
                "name": data['name'],
                "email": data['email'],
                "age": data['age'],  
                "message": "User created successfully"
            }), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already exists"}), 409
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({"error": "Database connection error"}), 500

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Retrieve all users"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age FROM users")
            rows = cursor.fetchall()
            
            users = []
            for row in rows:
                users.append({
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                })
            
            return jsonify({"users": users}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({"error": "Database connection error"}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a single user by ID"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                user = {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                }
                return jsonify({"user": user}), 200
            else:
                return jsonify({"error": "User not found"}), 404
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({"error": "Database connection error"}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user by ID"""
    if not request.json:
        abort(400, description="Request must be JSON")
    
    data = request.json
    validation_errors = validate_user_data(data)
    
    if validation_errors:
        return jsonify({"error": "Validation failed", "details": validation_errors}), 400
    
    conn = create_connection()
    if conn:
        try:
            # First check if user exists
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"error": "User not found"}), 404
            
            # Update user
            cursor.execute(
                "UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?",
                (data['name'], data['email'], data['age'], user_id)
            )
            conn.commit()
            
            # Return updated user
            cursor.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,))
            updated_row = cursor.fetchone()
            
            return jsonify({
                "user": {
                    "id": updated_row[0],
                    "name": updated_row[1],
                    "email": updated_row[2],
                    "age": updated_row[3]
                },
                "message": "User updated successfully"
            }), 200
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already exists"}), 409
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({"error": "Database connection error"}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    conn = create_connection()
    if conn:
        try:
            # First check if user exists
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if not row:
                return jsonify({"error": "User not found"}), 404
            
            # Delete user
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            
            return jsonify({"message": "User deleted successfully"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            conn.close()
    
    return jsonify({"error": "Database connection error"}), 500

if __name__ == '__main__':
    app.run(debug=True)