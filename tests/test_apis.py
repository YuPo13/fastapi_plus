import sys
import os
import pytest
from fastapi.testclient import TestClient
from db import Base, SessionLocal, engine
from main import app, get_db
from models import Author, Book
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
TEST_DATABASE_URL = "sqlite:///:memory:"

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Drop tables after test

@pytest.fixture(scope="function")
def client(db):
    """Creates a FastAPI test client with overridden database dependency."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_author(client, db):
    response = client.post("/authors/", json={"name": "Ілларіон", "surname": "Павлюк", "country": "Ukraine"})
    # assert response.status_code == 200
    assert "message" in response.json()
    assert "Ілларіон Павлюк" in response.json()["message"]


def test_get_authors(client):
    response = client.get("/authors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_author(client, db):
    # Create an author
    author = Author(name="George", surname="Orwell", country="United Kingdom")
    db.add(author)
    db.commit()

    # Delete the author
    response = client.delete(f"/authors/{author.id}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert f"Author with id {author.id} is deleted." in response.json()["message"]

def test_delete_nonexistent_author(client):
    response = client.delete("/authors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Author with id 999 not found"

def test_create_book(client, db):
    # First, create an author
    author = Author(name="Fredrik", surname="Backman", country="Sweden")
    db.add(author)
    db.commit()

    # Then, create a book linked to the author
    response = client.post("/books/", json={"title": "Anxious People", "author_id": author.id, "published_year": 2019})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Anxious People" in response.json()["message"]
    #Not to have test data in actual db
    db.delete(author)
    db.commit()


def test_create_book_invalid_author(client, db):
    response = client.post("/books/", json={"title": "Unknown Book", "author_id": 999, "published_year": 2000})
    assert response.status_code == 400
    assert "Author does not exist" in response.json()["detail"]


def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_book(client, db):
    # Create an author
    author = Author(name="George", surname="Orwell", country="United Kingdom")
    db.add(author)
    db.commit()

    # Delete the author
    response = client.delete(f"/authors/{author.id}")
    assert response.status_code == 200
    assert "message" in response.json()
    assert f"Author with id {author.id} is deleted." in response.json()["message"]

def test_delete_nonexistent_author(client):
    response = client.delete("/authors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Author with id 999 not found"