from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

#import  your routers below and follow the format 
from app.routers.users import app as user_app
from app.routers.auth import app as auth_router
from app.routers.lunch import app as lunch_app


api = APIRouter(prefix="/api")

#include your imported router to the api router
api.include_router(user_app)
api.include_router(lunch_app)
api.include_router(auth_router)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api)

@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
