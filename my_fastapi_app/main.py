from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models.database import engine, Base
from controllers import user

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(user.router)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
