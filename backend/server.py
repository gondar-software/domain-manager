from fastapi import FastAPI
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from src.api import api_router
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=settings.SERVER_PORT,
        reload=False
    )