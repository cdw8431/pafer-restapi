from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from crud import crud_user as crud
from schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("", response_model=List[User])
def read_uesrs(db: Session = Depends(deps.get_db)) -> Any:
    return crud.get_users(db)


@router.get("/{user_id}", response_model=User)
def read_user_by_id(db: Session = Depends(deps.get_db), user_id: int = None) -> Any:
    return crud.get_user_by_id(db, user_id)


@router.post("", response_model=User)
def create_user(db: Session = Depends(deps.get_db), user_in: UserCreate = None) -> Any:
    user = crud.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="This email already exists.")
    return crud.post_user(db, user_in)


@router.put("/{user_id}")
def update_user(
    db: Session = Depends(deps.get_db), user_id: int = None, user_in: UserUpdate = None
) -> Dict[str, str]:
    crud.update_user_by_id(db, user_id, user_in)
    return {"msg": "success"}


@router.delete("/{user_id}")
def delete_user_by_id(
    db: Session = Depends(deps.get_db), user_id: int = None
) -> Dict[str, str]:
    crud.delete_user_by_id(db, user_id)
    return {"msg": "success"}
