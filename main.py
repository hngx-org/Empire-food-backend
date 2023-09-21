from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.auth import app as auth_router
from app.routers.users import app as user_app
from app.routers.bank_account import router as bank_details


api = APIRouter(prefix="/api")

api.include_router(user_app)
api.include_router(auth_router)

# Added by Neon
api.include_router(bank_details)

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


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
