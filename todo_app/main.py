from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from database import engine, SessionLocal, Base
from models import Todo

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TodoRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.post("/items", response_model=TodoResponse)
def add_item(item: TodoRequest, db: Session = Depends(get_db)):
    todo = Todo(title=item.title, description=item.description, completed=item.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/items", response_model=List[TodoResponse])
def read_items(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.get("/items/{item_id}", response_model=TodoResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == item_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return todo

@app.put("/items/{item_id}", response_model=TodoResponse)
def edit_item(item_id: int, item: TodoRequest, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == item_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")

    todo.title = item.title
    todo.description = item.description
    todo.completed = item.completed
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/items/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == item_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(todo)
    db.commit()
    return {"message": "Item deleted"}
