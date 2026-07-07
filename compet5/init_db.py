import sys
import os

# Добавляем корневую папку проекта (на уровень выше compet5)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compet5.db.db import SessionLocal, engine, Base
from compet5.db import crud

def init_database():
    print("Создание таблиц в БД...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы!\n")
    db = SessionLocal()

    try:
        if crud.get_all_categories(db):
            print("Данные уже существуют в БД. Пропускаем инициализацию.")
            return

        print("Добавление категорий...")
        category1 = crud.create_category(db, "Фантастика")
        category2 = crud.create_category(db, "Детектив")
        category3 = crud.create_category(db, "Классика")
        print(f"Созданы категории: {category1.title}, {category2.title}, {category3.title}\n")
        print("Добавление книг...")

        books_data = [
            ("1984", "Антиутопия о тоталитарном обществе", 450.00, 1),
            ("451 градус по Фаренгейту", "Мир, где книги запрещены", 520.00, 1),
            ("Дюна", "Эпическая сага о планете Арракис", 890.00, 1),
            ("Нейромант", "Киберпанк-роман о виртуальной реальности", 670.00, 1),
            ("Убийство в Восточном экспрессе", "Классический детектив Агаты Кристи", 380.00, 2),
            ("Десять негритят", "Загадочные убийства на острове", 420.00, 2),
            ("Собака Баскервилей", "Приключения Шерлока Холмса", 350.00, 2),
            ("Война и мир", "Эпопея о жизни русского общества", 750.00, 3),
            ("Преступление и наказание", "Роман о морали и искуплении", 580.00, 3),
            ("Мастер и Маргарита", "Мистический роман Михаила Булгакова", 630.00, 3),
            ("Анна Каренина", "Трагическая история любви", 500.00, 3),
        ]
        
        for title, description, price, category_id in books_data:
            crud.create_book(
                db=db,
                title=title,
                description=description,
                price=price,
                category_id=category_id
            )
            print(f"  Добавлена книга: '{title}' (категория ID: {category_id})")
        
        print("\nБаза данных успешно инициализирована!")

    except Exception as e:
        print(f"Ошибка при инициализации БД: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()