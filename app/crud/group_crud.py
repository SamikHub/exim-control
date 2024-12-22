from sqlalchemy.orm import Session
from app.models.group_model import Group
from app.schemas.group_schema import GroupCreate, GroupUpdate

def get_group_by_name(db: Session, name: str):
    return db.query(Group).filter(Group.name == name).first()

def get_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group: GroupUpdate):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        return None
    db_group.name = group.name
    db.commit()
    db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group is None:
        return None
    db.delete(db_group)
    db.commit()
    return db_group