from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/search")
async def search(name_or_email: str = ""):
    return []

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)