from fastapi import FastAPI, APIRouter

from app.api.v1 import api


app = FastAPI()
app_router = APIRouter()


@app_router.get("/")
def root():
    return {"message": "Successful"}

app.include_router(app_router)
app.include_router(api.api_router)

