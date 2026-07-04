from fastapi import FastAPI
from app.api import books, categories

app = FastAPI(
    title="Library API",
    description="API for managing books and categories",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(books.router)
app.include_router(categories.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}