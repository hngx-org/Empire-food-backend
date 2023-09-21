from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.lunch import app as lunch_app
from app.routers.users import app as user_app


api = APIRouter(prefix="/api")

api.include_router(user_app)

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
app.include_router(lunch_app)

@app.get("/")
async def index():
    return { "status_code":200, "message":"success"}
    


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)