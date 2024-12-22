from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

class GroupOut(GroupBase):
    id: int

    class Config:
        orm_mode = True