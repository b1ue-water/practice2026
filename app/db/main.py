import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import SessionLocal
from db.crud import get_all_categories, get_all_books

def display_data():
    db = SessionLocal()
    try:
        print("=" * 50)
        print("Список категорий:")
        categories = get_all_categories(db)
        for cat in categories:
            print(f"  {cat.id}: {cat.title}")
            books = cat.books
            if books:
                print("    Книги:")
                for book in books:
                    print(f"      - {book.title} (цена: {book.price})")
            else:
                print("    (книг нет)")
        print("=" * 50)

        print("Все книги:")
        all_books = get_all_books(db)
        for b in all_books:
            print(f"  {b.id}: {b.title} | {b.price} | категория: {b.category.title}")
            
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    display_data()