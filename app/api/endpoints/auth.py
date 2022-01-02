from typing import Dict

from api import deps
from core.security import create_access_token, get_password_verify
from crud import crud_user as crud
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import UserAuth
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login")
def login(user_in: UserAuth, db: Session = Depends(deps.get_db)) -> Dict[str, str]:
    email, password = user_in.email, user_in.password
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404)
    elif not get_password_verify(password, user.password):
        raise HTTPException(status_code=403)
    return {"access_token": create_access_token({"sub": email})}
