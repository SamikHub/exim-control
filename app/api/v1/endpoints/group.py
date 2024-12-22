from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.group_schema import GroupCreate, GroupOut, GroupUpdate
from app.schemas.user_schema import UserOut  # Import UserOut
from app.crud.group_crud import create_group, get_group_by_name, get_groups, update_group, delete_group
from app.db.session import get_db
from app.core.security import get_current_admin

router = APIRouter()

@router.post("/", response_model=GroupOut)
def create_new_group(group: GroupCreate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_group = get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")
    return create_group(db=db, group=group)

@router.get("/", response_model=list[GroupOut])
def read_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups

@router.put("/{group_id}", response_model=GroupOut)
def update_existing_group(group_id: int, group: GroupUpdate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_group = update_group(db, group_id=group_id, group=group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.delete("/{group_id}", response_model=GroupOut)
def delete_existing_group(group_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_admin)):
    db_group = delete_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group