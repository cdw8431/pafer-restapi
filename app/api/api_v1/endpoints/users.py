from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from crud import crud_user as crud
from schemas.user import UserRes

router = APIRouter()


@router.get("", response_model=List[UserRes])
def read_uesrs(db: Session = Depends(deps.get_db)) -> Any:
    return crud.get_users(db)
