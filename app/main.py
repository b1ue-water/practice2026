from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import books, categories
from app.db.db import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="API for managing books and categories",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(categories.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Service is running"}

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Book API",
        "docs": "/docs",
        "health": "/health"
    }