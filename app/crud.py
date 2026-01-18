import models
from sqlalchemy.orm import Session
from models import Term
from schemas import TermCreate, TermUpdate
from sqlalchemy import literal


def get_terms(db: Session):
    return db.query(models.Term).all()

def get_term_by_keyword(db: Session, keyword: str):
    return db.query(Term).filter(Term.keyword == literal(keyword)).first()


def create_term(db: Session, term: TermCreate):
    try:
        db_term = Term(**term.dict())
        db.add(db_term)
        db.commit()
        db.refresh(db_term)
        return db_term
    except Exception:
        db.rollback()
        raise


def update_term(db: Session, db_term: Term, updates: TermUpdate):
    try:
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(db_term, key, value)
        db.commit()
        db.refresh(db_term)
        return db_term
    except Exception:
        db.rollback()
        raise


def delete_term(db: Session, db_term: Term):
    try:
        db.delete(db_term)
        db.commit()
    except Exception:
        db.rollback()
        raise
