# MJ - Biochemistry AI Tool
# Authentication Module

import hashlib
import json
from datetime import datetime
from database import get_database_connection
from utils import log_message

class UserManager:
    """Manage user accounts and authentication"""
    
    @staticmethod
    def hash_password(password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create_user(username, email, password):
        """Create a new user account"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            hashed_password = UserManager.hash_password(password)
            
            cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            log_message(f"User created: {username}")
            return {"success": True, "user_id": user_id}
        
        except Exception as e:
            log_message(f"Error creating user: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def verify_user(username, password):
        """Verify user credentials"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            hashed_password = UserManager.hash_password(password)
            
            cursor.execute('''
            SELECT id, username, email FROM users
            WHERE username = ? AND password_hash = ?
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                log_message(f"User verified: {username}")
                return {"success": True, "user_id": user[0], "username": user[1]}
            else:
                return {"success": False, "error": "Invalid credentials"}
        
        except Exception as e:
            log_message(f"Error verifying user: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user information by ID"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, username, email, created_at FROM users
            WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "created_at": user[3]
                }
            return None
        
        except Exception as e:
            log_message(f"Error getting user: {str(e)}", "ERROR")
            return None
    
    @staticmethod
    def list_all_users():
        """List all users (admin only)"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, username, email, created_at FROM users
            ''')
            
            users = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "created_at": user[3]
                }
                for user in users
            ]
        
        except Exception as e:
            log_message(f"Error listing users: {str(e)}", "ERROR")
            return []

if __name__ == "__main__":
    # Test
    print("Auth module loaded successfully")
