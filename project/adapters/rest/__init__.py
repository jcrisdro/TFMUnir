from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project.adapters.rest.v1 import router as v1

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1, prefix="/v1")
