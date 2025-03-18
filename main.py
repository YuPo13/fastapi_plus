from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import engine, SessionLocal, Base
from models import Author, Book
from schemas import AuthorCreate, BookCreate

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/authors/")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name, surname=author.surname, country=author.country)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return {"message": f"The following author was created: {db_author.name} {db_author.surname}."}

@app.get("/authors/")
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@app.post("/books/")
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author_id=book.author_id, published_year=book.published_year)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"message": f"The following book was created: {db_book.title}."}

@app.get("/books/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.delete("/authors/{author_id}")
def delete_author_by_id(author_id: int, db: Session = Depends(get_db)):
    author_to_be_deleted = db.query(Author).filter(Author.id == author_id).first()
    if not author_to_be_deleted:
        raise HTTPException(status_code=404, detail=f"Book with ID {author_id} not found.")

    db.delete(author_to_be_deleted)
    db.commit()
    return {"message": f"Authors with ids {author_id} is deleted."}