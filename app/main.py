from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from routers import authentications, notifications, organizations, transactions, users
import uvicorn
import models
import db


models.Base.metadata.create_all(bind=db.engine)


app = FastAPI()

# To be updated as seen necessary
origins = ["*"]

app.add_middleware(
    AuthenticationMiddleware,
    # you can auth for token stored in a cookie if we choose this route
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(authentications.router)
app.include_router(notifications.router)
app.include_router(organizations.router)
app.include_router(transactions.router)
app.include_router(users.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
