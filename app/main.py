from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.api.v1.endpoints import example, user, group, auth
from app.db.init_db import init_db
from app.db.session import get_db  # Import get_db
from app.middleware import AuthMiddleware
from app.core.security import create_access_token, verify_password
from app.utils.user_utils import get_user_by_username

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(example.router, prefix="/example", tags=["example"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(group.router, prefix="/groups", tags=["groups"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("panel.html", {"request": request})

@app.get("/auth/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/auth/login", response_class=HTMLResponse)
async def login_for_access_token(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.post("/auth/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response