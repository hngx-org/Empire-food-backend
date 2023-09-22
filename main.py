from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.auth import app as auth_router
from app.routers.lunch import app as lunch_app
from app.routers.users import app as user_app
from app.routers.bank_account import router as bank_details
from app.db.database import create_database


v1 = APIRouter(prefix="/api/v1")

############################# include all routers here #############################
v1.include_router(lunch_app)
v1.include_router(user_app)
v1.include_router(auth_router)
# Added by Neon
v1.include_router(bank_details)
####################################################################################

@v1.get("/health")
async def health():
    return {"status": "ok"}



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

app.include_router(v1)


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
