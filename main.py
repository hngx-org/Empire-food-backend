from fastapi import FastAPI
import uvicorn
from app.routers.users import app as user_app
from app.routers import auth
app = FastAPI()


app.include_router(user_app)
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
