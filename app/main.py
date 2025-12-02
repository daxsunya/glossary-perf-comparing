from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Glossary API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/terms", response_model=list[schemas.Term])
def read_terms(db: Session = Depends(get_db)):
    return crud.get_terms(db)


@app.get("/terms/{keyword}", response_model=schemas.Term)
def read_term(keyword: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(404, "Term not found")
    return term


@app.post("/terms", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    exists = crud.get_term_by_keyword(db, term.keyword)
    if exists:
        raise HTTPException(400, "Term already exists")
    return crud.create_term(db, term)


@app.put("/terms/{keyword}", response_model=schemas.Term)
def update_term(keyword: str, updates: schemas.TermUpdate, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(404, "Term not found")
    return crud.update_term(db, term, updates)


@app.delete("/terms/{keyword}")
def delete_term(keyword: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(404, "Term not found")
    crud.delete_term(db, term)
    return {"message": "Deleted"}
