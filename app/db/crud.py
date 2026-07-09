from sqlalchemy.orm import Session
from app.db import models
from typing import Optional

def create_category(db: Session, title: str):
    """Создание категории"""
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int):
    """Получение категории по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_title(db: Session, title: str):
    """Получение категории по названию"""
    return db.query(models.Category).filter(models.Category.title == title).first()

def get_all_categories(db: Session):
    """Получение всех категорий"""
    return db.query(models.Category).all()

def update_category(db: Session, category_id: int, title: str):
    """Обновление категории"""
    category = get_category(db, category_id)
    if category:
        category.title = title
        db.commit()
        db.refresh(category)
        return category
    return None

def delete_category(db: Session, category_id: int):
    """Удаление категории"""
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = ""):
    """Создание книги"""
    book = models.Book(
        title=title,
        description=description,
        price=price,
        url=url,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int):
    """Получение книги по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int):
    """Получение книг по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def get_all_books(db: Session):
    """Получение всех книг"""
    return db.query(models.Book).all()

def update_book(db: Session, book_id: int, title: Optional[str] = None, 
                description: Optional[str] = None, price: Optional[float] = None, 
                url: Optional[str] = None, category_id: Optional[int] = None):
    """
    Обновление книги.
    Можно обновить любое поле или несколько полей одновременно.
    Передаем только те поля, которые хотим изменить.
    """
    book = get_book(db, book_id)
    if not book:
        return None

    if title is not None:
        book.title = title
    if description is not None:
        book.description = description
    if price is not None:
        book.price = price
    if url is not None:
        book.url = url
    if category_id is not None:
        book.category_id = category_id
    
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    """Удаление книги"""
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return True
    return False

def get_books_with_category(db: Session):
    """Получение всех книг с названиями категорий (JOIN)"""
    return db.query(models.Book, models.Category.title.label("category_title"))\
        .join(models.Category, models.Book.category_id == models.Category.id)\
        .all()