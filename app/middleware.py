from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from jose import JWTError, jwt
from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path not in ["/auth/login", "/auth/login/"]:
            token = request.cookies.get("access_token")
            if not token:
                return RedirectResponse(url="/auth/login")
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                username: str = payload.get("sub")
                if username is None:
                    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            except JWTError:
                return RedirectResponse(url="/auth/login")
        response = await call_next(request)
        return response