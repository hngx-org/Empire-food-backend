from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers.auth import app as auth_router
from app.routers.lunch import app as lunch_app
from app.routers.users import app as user_app
from app.routers.organizations import router as org_signup
from app.routers.lunch import app as lunch_app


v1 = APIRouter(prefix="/api/v1")
############################# include all routers here #############################
v1.include_router(lunch_app)
v1.include_router(user_app)
v1.include_router(auth_router)
<<<<<<< HEAD
v1.include_router(lunch_router)
||||||| 7ed8fd9
=======
v1.include_router(org_signup)
>>>>>>> f4ebd45b1da61adfe35793ad929561d5b5d3bdc5
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
