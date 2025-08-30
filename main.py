from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
