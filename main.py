from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
import os
from dotenv import load_dotenv

from database import engine, get_db
from models import Base
from schemas import *
from crud import *

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Mahadeva Electronics API",
    description="FastAPI backend for Mahadeva Electronics website",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Custom documentation route
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

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

@app.get("/test-db-access")
async def test_db_access():
    """Test database access without complex operations"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"message": "Database access working", "status": "success"}
    except Exception as e:
        return {"message": "Database access failed", "error": str(e)}

@app.get("/test-crud-import")
async def test_crud_import():
    """Test if CRUD functions can be imported"""
    try:
        from crud import get_all_products, create_new_product, update_existing_product, delete_existing_product
        return {"message": "All CRUD functions imported successfully"}
    except Exception as e:
        return {"message": "CRUD import failed", "error": str(e)}

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

# Product routes
@app.get("/api/products/", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@app.post("/api/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_new_product(db, product)

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated_product = update_existing_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_existing_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Part routes
@app.get("/api/parts/", response_model=List[PartResponse])
async def get_parts(db: Session = Depends(get_db)):
    return get_all_parts(db)

@app.post("/api/parts/", response_model=PartResponse)
async def create_part(part: PartCreate, db: Session = Depends(get_db)):
    return create_new_part(db, part)

@app.get("/api/parts/{part_id}", response_model=PartResponse)
async def get_part(part_id: int, db: Session = Depends(get_db)):
    part = get_part_by_id(db, part_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

@app.put("/api/parts/{part_id}", response_model=PartResponse)
async def update_part(part_id: int, part: PartUpdate, db: Session = Depends(get_db)):
    updated_part = update_existing_part(db, part_id, part)
    if not updated_part:
        raise HTTPException(status_code=404, detail="Part not found")
    return updated_part

@app.delete("/api/parts/{part_id}")
async def delete_part(part_id: int, db: Session = Depends(get_db)):
    success = delete_existing_part(db, part_id)
    if not success:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part deleted successfully"}

# Technician routes
@app.get("/api/technicians/", response_model=List[TechnicianResponse])
async def get_technicians(db: Session = Depends(get_db)):
    return get_all_technicians(db)

@app.post("/api/technicians/", response_model=TechnicianResponse)
async def create_technician(technician: TechnicianCreate, db: Session = Depends(get_db)):
    return create_new_technician(db, technician)

@app.put("/api/technicians/{technician_id}", response_model=TechnicianResponse)
async def update_technician(technician_id: int, technician: TechnicianUpdate, db: Session = Depends(get_db)):
    updated_technician = update_existing_technician(db, technician_id, technician)
    if not updated_technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    return updated_technician

@app.delete("/api/technicians/{technician_id}")
async def delete_technician(technician_id: int, db: Session = Depends(get_db)):
    success = delete_existing_technician(db, technician_id)
    if not success:
        raise HTTPException(status_code=404, detail="Technician not found")
    return {"message": "Technician deleted successfully"}

# Booking routes
@app.get("/api/bookings/", response_model=List[BookingResponse])
async def get_bookings(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@app.post("/api/bookings/", response_model=BookingResponse)
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_new_booking(db, booking)

@app.put("/api/bookings/{booking_id}", response_model=BookingResponse)
async def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    updated_booking = update_existing_booking(db, booking_id, booking)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@app.delete("/api/bookings/{booking_id}")
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    success = delete_existing_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted successfully"}

# Feedback routes
@app.get("/api/feedback/", response_model=List[FeedbackResponse])
async def get_feedback(db: Session = Depends(get_db)):
    return get_all_feedback(db)

@app.post("/api/feedback/", response_model=FeedbackResponse)
async def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    return create_new_feedback(db, feedback)

@app.put("/api/feedback/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(feedback_id: int, feedback: FeedbackUpdate, db: Session = Depends(get_db)):
    updated_feedback = update_existing_feedback(db, feedback_id, feedback)
    if not updated_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return updated_feedback

@app.delete("/api/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    success = delete_existing_feedback(db, feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}

# Authentication routes
@app.post("/api/auth/token/")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
