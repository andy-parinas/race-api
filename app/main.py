from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api


app = FastAPI()
app_router = APIRouter()

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


@app_router.get("/")
def root():
    return {"message": "Successful"}


app.include_router(app_router)
app.include_router(api.api_router)
