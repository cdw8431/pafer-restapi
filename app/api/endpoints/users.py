from typing import Any, Dict, List

from api import deps
from crud import crud_user as crud
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import User, UserAuth, UserPasswordChange, UserToken
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("", response_model=List[User])
def read_uesrs(db: Session = Depends(deps.get_db)) -> Any:
    return crud.get_users(db)


@router.get("/{user_id}", response_model=User)
def read_user_by_id(user_id: int, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@router.get("/email/{user_email}", response_model=User)
def read_user_by_email(user_email: str, db: Session = Depends(deps.get_db)) -> Any:
    user = crud.get_user_by_email(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="This user is not exists.")
    return user


@router.post("", response_model=UserToken, status_code=201)
def create_user(
    user_in: UserAuth, db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    user = crud.get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="This email already exists.")
    return {"access_token": crud.post_user(db, user_in)}


@router.patch("/{user_id}/change-password")
def update_user_password(
    user_id: int, user_in: UserPasswordChange, db: Session = Depends(deps.get_db)
) -> Dict[str, str]:
    result: int = crud.update_user_password_by_id(db, user_id, user_in)
    if not result:
        raise HTTPException(status_code=401, detail="Password does not match.")
    elif result == 2:
        raise HTTPException(status_code=404)
    return {"msg": "success"}


@router.delete("/{user_id}", status_code=204)
def delete_user_by_id(user_id: int, db: Session = Depends(deps.get_db)) -> None:
    crud.delete_user_by_id(db, user_id)
