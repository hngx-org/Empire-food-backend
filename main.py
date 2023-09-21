from fastapi import FastAPI
import uvicorn
from app.routers.lunch import app as lunch_app
app = FastAPI()

app.include_router(lunch_app)


@app.get("/")
async def index():
    return { "status_code":200, "message":"success"}
    


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)