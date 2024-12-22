from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine
from app.models import user_model, group_model

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Створення таблиць у базі даних
    user_model.Base.metadata.create_all(bind=engine)
    group_model.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

app.include_router(api_router, prefix="/api/v1")