import random
import string
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl

from database import Base, engine, SessionLocal
from models import ShortURL

Base.metadata.create_all(bind=engine)

app = FastAPI()

class UrlRequest(BaseModel):
    url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def make_short_id():
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(6))

@app.post("/shorten")
def create_short_url(data: UrlRequest, db: Session = Depends(get_db)):
    short_id = make_short_id()
    new_url = ShortURL(short_id=short_id, full_url=str(data.url))
    db.add(new_url)
    db.commit()
    return {"short_url": f"http://localhost:8001/{short_id}"}

@app.get("/{short_id}")
def open_url(short_id: str, db: Session = Depends(get_db)):
    url = db.query(ShortURL).filter(ShortURL.short_id == short_id).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.full_url)

@app.get("/stats/{short_id}")
def url_info(short_id: str, db: Session = Depends(get_db)):
    url = db.query(ShortURL).filter(ShortURL.short_id == short_id).first()
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"short_id": url.short_id, "full_url": url.full_url}
