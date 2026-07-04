from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud
from app.db.db import get_db
from app import schemas

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    if category_id is not None:
        category = crud.get_category(db, category_id)
        if category is None:
            raise HTTPException(status_code=400, detail="Category does not exist")
        return crud.get_books_by_category(db, category_id)
    return crud.get_all_books(db)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    category = crud.get_category(db, book.category_id)
    if category is None:
        raise HTTPException(status_code=400, detail="Category does not exist")
    
    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or ""
    )

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    if book.category_id is not None:
        category = crud.get_category(db, book.category_id)
        if category is None:
            raise HTTPException(status_code=400, detail="Category does not exist")

    update_data = {k: v for k, v in book.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    db_book = crud.update_book(db, book_id, **update_data)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return None