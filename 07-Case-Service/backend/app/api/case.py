from fastapi import APIRouter, HTTPException
from app.models.case_model import Case
from app.database import SessionLocal

router = APIRouter()

@router.post("/cases")
def create_case(title: str, description: str = ""):
    db = SessionLocal()
    new_case = Case(title=title, description=description)
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    db.close()
    return new_case

@router.get("/cases/{case_id}")
def get_case(case_id: int):
    db = SessionLocal()
    case = db.query(Case).filter(Case.id == case_id).first()
    db.close()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
