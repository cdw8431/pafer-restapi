from typing import Any, Dict, List

from api import deps
from crud import crud_user as crud
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import User, UserAuth, UserRegister, UserUpdate
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=List[User])
def read_uesrs(db: Session = Depends(deps.get_db)) -> Any:
    return crud.get_users(db)


@router.get("/{user_id}", response_model=User)
def read_user_by_id(user_id: int, db: Session = Depends(deps.get_db)) -> Any:
    return crud.get_user_by_id(db, user_id)


@router.post("/register", response_model=UserAuth)
def register_user(user_in: UserRegister, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="This email already exists.")
    return {"access_token": crud.post_user(db, user_in)}


@router.put("/{user_id}")
def update_user(
    user_id: int, user_in: UserUpdate, db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    crud.update_user_by_id(db, user_id, user_in)
    return {"msg": "success"}


@router.delete("/{user_id}")
def delete_user_by_id(
    user_id: int, db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    crud.delete_user_by_id(db, user_id)
    return {"msg": "success"}
