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
        
        # Try to connect
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return {"message": "Database connection successful!", "result": "connected"}
            
    except Exception as e:
        return {"message": f"Database connection error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
