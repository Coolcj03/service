from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Mahadeva Electronics API",
    description="FastAPI backend for Mahadeva Electronics website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Mahadeva Electronics API"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/test")
async def test():
    """Simple test endpoint"""
    return {"message": "Test endpoint working!"}

@app.get("/db-test")
async def db_test():
    """Test database connection"""
    try:
        # Import database module
        import database
        
        # Test if we can access the engine
        if hasattr(database, 'engine'):
            return {"message": "Database module imported successfully!", "engine": "found"}
        else:
            return {"message": "Database engine not found!"}
            
    except Exception as e:
        return {"message": f"Database import error: {str(e)}"}

@app.get("/db-connect")
async def db_connect():
    """Test actual database connection"""
    try:
        from database import engine
        from sqlalchemy import text
        
        # Try to connect with correct SQLAlchemy syntax
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"message": "Database connection successful!", "result": "connected"}
            
    except Exception as e:
        return {"message": f"Database connection error: {str(e)}"}

@app.get("/models-test")
async def models_test():
    """Test if database models can be imported"""
    try:
        # Try to import models
        from models import Base, Product, Part, Technician, Booking, Feedback, AdminUser
        
        return {
            "message": "All models imported successfully!",
            "models": ["Base", "Product", "Part", "Technician", "Booking", "Feedback", "AdminUser"]
        }
        
    except Exception as e:
        return {"message": f"Models import error: {str(e)}"}

@app.get("/schemas-test")
async def schemas_test():
    """Test if Pydantic schemas can be imported"""
    try:
        # Try to import schemas
        from schemas import (
            ProductBase, ProductCreate, ProductUpdate, ProductResponse,
            PartBase, PartCreate, PartUpdate, PartResponse,
            TechnicianBase, TechnicianCreate, TechnicianUpdate, TechnicianResponse,
            BookingBase, BookingCreate, BookingUpdate, BookingResponse,
            FeedbackBase, FeedbackCreate, FeedbackUpdate, FeedbackResponse,
            AdminUserBase, AdminUserCreate, AdminUserUpdate, AdminUserResponse,
            LoginRequest, TokenResponse
        )
        
        return {
            "message": "All schemas imported successfully!",
            "schemas": [
                "ProductBase", "ProductCreate", "ProductUpdate", "ProductResponse",
                "PartBase", "PartCreate", "PartUpdate", "PartResponse", 
                "TechnicianBase", "TechnicianCreate", "TechnicianUpdate", "TechnicianResponse",
                "BookingBase", "BookingCreate", "BookingUpdate", "BookingResponse",
                "FeedbackBase", "FeedbackCreate", "FeedbackUpdate", "FeedbackResponse",
                "AdminUserBase", "AdminUserCreate", "AdminUserUpdate", "AdminUserResponse",
                "LoginRequest", "TokenResponse"
            ]
        }
        
    except Exception as e:
        return {"message": f"Schemas import error: {str(e)}"}

@app.get("/crud-test")
async def crud_test():
    """Test if CRUD operations can be imported"""
    try:
        # Try to import CRUD functions step by step
        from crud import get_all_products
        from crud import get_all_parts
        from crud import get_all_technicians
        from crud import get_all_bookings
        from crud import get_all_feedback
        from crud import create_admin_user
        from crud import get_admin_user_by_email
        from crud import authenticate_user
        from crud import create_access_token
        from crud import verify_password
        from crud import get_password_hash
        
        return {
            "message": "All CRUD operations imported successfully!",
            "crud_functions": [
                "Product CRUD: get_all_products",
                "Part CRUD: get_all_parts", 
                "Technician CRUD: get_all_technicians",
                "Booking CRUD: get_all_bookings",
                "Feedback CRUD: get_all_feedback",
                "Admin CRUD: create_admin_user, get_admin_user_by_email, authenticate_user",
                "Auth: create_access_token, verify_password, get_password_hash"
            ]
        }
        
    except Exception as e:
        return {"message": f"CRUD import error: {str(e)}"}

@app.get("/crud-test-simple")
async def crud_test_simple():
    """Test basic CRUD imports one by one"""
    try:
        # Test each import individually
        result = {}
        
        try:
            from crud import get_all_products
            result["products"] = "✅ OK"
        except Exception as e:
            result["products"] = f"❌ {str(e)}"
            
        try:
            from crud import get_all_parts
            result["parts"] = "✅ OK"
        except Exception as e:
            result["parts"] = f"❌ {str(e)}"
            
        try:
            from crud import create_admin_user
            result["admin_create"] = "✅ OK"
        except Exception as e:
            result["admin_create"] = f"❌ {str(e)}"
            
        try:
            from crud import get_admin_user_by_email
            result["admin_get"] = "✅ OK"
        except Exception as e:
            result["admin_get"] = f"❌ {str(e)}"
            
        return {
            "message": "CRUD import test results",
            "results": result
        }
        
    except Exception as e:
        return {"message": f"Test error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
