from fastapi import FastAPI
import uvicorn
from auth.exports import auth_router, Base, engine

# 1. Create tables for the whole app
# This ensures that even if you plug this into a brand new app, 
# the 'users' table is created automatically in that app's database.
Base.metadata.create_all(bind=engine)

# 2. Initialize the Main App
app = FastAPI(title="My Pluggable App")

# 3. Plug in the Auth module
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Main Application is running with Auth plugged in!"}

# 4. The "Stay Alive" Block
if __name__ == "__main__":
    print("🚀 Starting Pluggable Server...")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=True  # Helpful for development
    )