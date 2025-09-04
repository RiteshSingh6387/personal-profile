from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from router import profile
from database import client  

app = FastAPI(
    title="profile API",
    description="API for managing personal profile data.",
    version="1.0.0"
)

# CORS (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])

# Startup logic
@app.on_event("startup")
async def startup():
    try:
        client["admin"].command("ping")   # ✅ correct
        print("✅ MongoDB connection established!")
        print("🚀 FastAPI is starting up...")
    except Exception as e:
        print("❌ MongoDB connection failed:", str(e))
        raise HTTPException(status_code=500, detail=f"Database connection error on startup: {e}")
        
    

# Shutdown logic
@app.on_event("shutdown")
async def shutdown():
    try:
        print("🛑 FastAPI is shutting down...")
        client.close()
        print("❌ MongoDB connection closed.")
    except Exception as e:
        print("❌ Error closing MongoDB connection:", str(e))
        raise HTTPException(status_code=500, detail=f"Database disconnection error on shutdown: {e}")
    
    

# Root path
@app.get("/")
async def root():
    return {"message": "Welcome to the Profile API"}








