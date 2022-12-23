from fastapi import FastAPI, APIRouter

app = FastAPI()
api_router = APIRouter()


@api_router.get("/")
def root():
    return {"message": "Successful"}

app.include_router(api_router)


