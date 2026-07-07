import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compet5.db.db import SessionLocal
from compet5.db import crud

def print_books_with_categories():
    db = SessionLocal()
    try:
        print("\n" + "="*70)
        print("КНИГИ И ИХ КАТЕГОРИИ")
        print("="*70 + "\n")
        categories = crud.get_all_categories(db)
        
        if not categories:
            print("В базе данных нет категорий. Запустите init_db.py сначала.")
            return
        
        for category in categories:
            print(f"\n📚 Категория: {category.title.upper()}")
            print("-" * 50)
            books = crud.get_books_by_category(db, category.id)
            
            if not books:
                print("  Книг в этой категории пока нет")
                continue
                
            for book in books:
                print(f"  📖 {book.title}")
                print(f"     Описание: {book.description[:80]}..." if len(book.description) > 80 else f"     Описание: {book.description}")
                print(f"     💰 Цена: {book.price:.2f} ₽")
                if book.url:
                    print(f"     🔗 {book.url}")
                print()
                
        print("="*70)
        print(f"Всего книг: {len(crud.get_all_books(db))}")
        print("="*70)
        
    except Exception as e:
        print(f"Ошибка при чтении данных: {e}")
    finally:
        db.close()

def main():
    print("\n" + "="*70)
    print("ДОБРО ПОЖАЛОВАТЬ В КАТАЛОГ КНИГ")
    print("="*70)
    print_books_with_categories()

if __name__ == "__main__":
    main()