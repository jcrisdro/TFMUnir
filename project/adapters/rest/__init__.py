from fastapi import FastAPI
from project.adapters.rest.v1 import router as v1


app = FastAPI()
app.include_router(v1, prefix="/v1")
