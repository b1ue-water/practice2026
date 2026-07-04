import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import engine, SessionLocal
from db import models
from db.crud import create_category, create_book

def init_db():
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    
    try:
        cat_fiction = create_category(db, "Художественная литература")
        cat_science = create_category(db, "Научно-популярная")
        cat_children = create_category(db, "Детские книги")

        create_book(db, "Война и мир", "Роман-эпопея Льва Толстого", 500.0, cat_fiction.id, "http://example.com/war")
        create_book(db, "Преступление и наказание", "Роман Достоевского", 450.0, cat_fiction.id, "http://example.com/crime")
        create_book(db, "Мастер и Маргарита", "Роман Булгакова", 600.0, cat_fiction.id, "http://example.com/master")

        create_book(db, "Краткая история времени", "Стивен Хокинг", 700.0, cat_science.id, "http://example.com/hawking")
        create_book(db, "Сам себе мозг", "Дэвид Иглмен", 650.0, cat_science.id, "http://example.com/brain")

        create_book(db, "Маленький принц", "Экзюпери", 350.0, cat_children.id, "http://example.com/prince")
        create_book(db, "Винни-Пух", "Милн", 400.0, cat_children.id, "http://example.com/pooh")
        create_book(db, "Гарри Поттер и философский камень", "Роулинг", 800.0, cat_children.id, "http://example.com/harry")
        
        print("База данных успешно инициализирована и наполнена тестовыми данными!")
        
    except Exception as e:
        print(f"Ошибка при инициализации: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()