import asyncio

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import schemas
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Glossary API")

REQUEST_TIMEOUT = 20.0


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        return await asyncio.wait_for(
            call_next(request),
            timeout=REQUEST_TIMEOUT
        )
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"detail": "Request timeout exceeded"}
        )


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.get("/terms", response_model=list[schemas.Term])
def read_terms(db: Session = Depends(get_db)):
    return crud.get_terms(db)


@app.get("/terms/{keyword}", response_model=schemas.Term)
def read_term(keyword: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(
            status_code=404,
            detail="Term not found"
        )
    return term


@app.post("/terms", response_model=schemas.Term)
def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    exists = crud.get_term_by_keyword(db, term.keyword)
    if exists:
        raise HTTPException(
            status_code=400,
            detail="Term already exists"
        )
    return crud.create_term(db, term)


@app.put("/terms/{keyword}", response_model=schemas.Term)
def update_term(
    keyword: str,
    updates: schemas.TermUpdate,
    db: Session = Depends(get_db)
):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(
            status_code=404,
            detail="Term not found"
        )
    return crud.update_term(db, term, updates)


@app.delete("/terms/{keyword}", status_code=204)
def delete_term(keyword: str, db: Session = Depends(get_db)):
    term = crud.get_term_by_keyword(db, keyword)
    if not term:
        raise HTTPException(
            status_code=404,
            detail="Term not found"
        )
    crud.delete_term(db, term)
    return Response(status_code=204)
