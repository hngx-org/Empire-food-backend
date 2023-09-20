from fastapi import FastAPI
import uvicorn
from app.routers.users import app as user_app

app = FastAPI()

app.include_router(user_app)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
