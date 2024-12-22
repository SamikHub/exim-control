from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate
from app.crud.user_crud import create_user, get_users, update_user, delete_user
from app.db.session import get_db
from app.core.security import get_current_admin
from app.utils.user_utils import get_user_by_username

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@router.get("/", response_model=list[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=UserOut)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_existing_user(user_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user