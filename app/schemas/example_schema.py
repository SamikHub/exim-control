from pydantic import BaseModel

class ExampleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
