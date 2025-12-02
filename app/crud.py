from sqlalchemy.orm import Session
import models
import schemas


def get_terms(db: Session):
    return db.query(models.Term).all()


def get_term_by_keyword(db: Session, keyword: str):
    return db.query(models.Term).filter(models.Term.keyword == keyword).first()


def create_term(db: Session, term: schemas.TermCreate):
    db_term = models.Term(**term.dict())
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term


def update_term(db: Session, db_term: models.Term, updates: schemas.TermUpdate):
    if updates.keyword is not None:
        db_term.keyword = updates.keyword
    if updates.description is not None:
        db_term.description = updates.description

    db.commit()
    db.refresh(db_term)
    return db_term


def delete_term(db: Session, db_term: models.Term):
    db.delete(db_term)
    db.commit()
    return True
