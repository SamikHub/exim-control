from fastapi import APIRouter
from app.schemas.example_schema import ExampleSchema

router = APIRouter()

@router.get("/", response_model=ExampleSchema)
def read_example():
    return {"id": 1, "name": "Example"}
