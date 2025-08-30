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
        # Try to import CRUD functions
        from crud import (
            # Product CRUD
            get_all_products, get_product_by_id, create_new_product, 
            update_existing_product, delete_existing_product,
            # Part CRUD
            get_all_parts, get_part_by_id, create_new_part,
            update_existing_part, delete_existing_part,
            # Technician CRUD
            get_all_technicians, get_technician_by_id, create_new_technician,
            update_existing_technician, delete_existing_technician,
            # Booking CRUD
            get_all_bookings, get_booking_by_id, create_new_booking,
            update_existing_booking, delete_existing_booking,
            # Feedback CRUD
            get_all_feedback, get_feedback_by_id, create_new_feedback,
            update_existing_feedback, delete_existing_feedback,
            # Admin CRUD
            get_admin_by_email, create_admin_user, authenticate_user,
            # Auth functions
            create_access_token, verify_password, get_password_hash
        )
        
        return {
            "message": "All CRUD operations imported successfully!",
            "crud_functions": [
                "Product CRUD: get_all_products, get_product_by_id, create_new_product, update_existing_product, delete_existing_product",
                "Part CRUD: get_all_parts, get_part_by_id, create_new_part, update_existing_part, delete_existing_part",
                "Technician CRUD: get_all_technicians, get_technician_by_id, create_new_technician, update_existing_technician, delete_existing_technician",
                "Booking CRUD: get_all_bookings, get_booking_by_id, create_new_booking, update_existing_booking, delete_existing_booking",
                "Feedback CRUD: get_all_feedback, get_feedback_by_id, create_new_feedback, update_existing_feedback, delete_existing_feedback",
                "Admin CRUD: get_admin_by_email, create_admin_user, authenticate_user",
                "Auth: create_access_token, verify_password, get_password_hash"
            ]
        }
        
    except Exception as e:
        return {"message": f"CRUD import error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
