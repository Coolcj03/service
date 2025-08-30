#!/usr/bin/env python3
"""
Database initialization script for Mahadeva Electronics FastAPI backend.
Run this script manually to create database tables and initial admin user.
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_database, test_connection, SessionLocal
from models import Base, AdminUser
from crud import create_admin_user, get_admin_by_email
from passlib.context import CryptContext

load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def main():
    """Main initialization function"""
    print("🚀 Starting database initialization...")
    
    # Test database connection first
    print("📡 Testing database connection...")
    if not test_connection():
        print("❌ Database connection failed. Please check your DATABASE_URL.")
        print("💡 Make sure your PostgreSQL service is running on Railway.")
        return False
    
    # Initialize database tables
    print("🗄️  Creating database tables...")
    if not init_database():
        print("❌ Failed to create database tables.")
        return False
    
    # Create initial admin user
    print("👤 Setting up initial admin user...")
    try:
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = get_admin_by_email(db, "admin@mahadeva.com")
        if existing_admin:
            print("✅ Admin user already exists.")
            return True
        
        # Create default admin user
        admin_data = {
            "email": os.getenv("ADMIN_EMAIL", "admin@mahadeva.com"),
            "password": os.getenv("ADMIN_PASSWORD", "admin123"),
            "full_name": "System Administrator"
        }
        
        admin_user = create_admin_user(db, admin_data)
        if admin_user:
            print(f"✅ Admin user created successfully: {admin_user.email}")
            print("🔑 Default credentials:")
            print(f"   Email: {admin_data['email']}")
            print(f"   Password: {admin_data['password']}")
            print("⚠️  Please change the password after first login!")
        else:
            print("❌ Failed to create admin user.")
            return False
            
    except Exception as e:
        print(f"❌ Error during admin user setup: {e}")
        return False
    finally:
        db.close()
    
    print("🎉 Database initialization completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
