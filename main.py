from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.auth import app as auth_router
from app.routers.lunch import app as lunch_app
from app.routers.users import app as user_app
from app.routers.organizations import router as org_signup
from app.routers.lunch import app as lunch_app
from app.db.database import create_database
from decouple import config

prod = True if config("PROD", default = "dev")  == "PRODUCTION" else False

v1 = APIRouter(prefix="/api/v1")
############################# include all routers here #############################
v1.include_router(lunch_app)
v1.include_router(user_app)
v1.include_router(auth_router)
v1.include_router(org_signup)
####################################################################################
@v1.get("/health")
async def health():
    return {"status": "ok"}


app = FastAPI()

if not prod:
    create_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
