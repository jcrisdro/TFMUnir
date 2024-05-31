import os

from fastapi import Depends, FastAPI

from project.adapters.rest.v1.files import FilesRestAdapter
from project.adapters.rest.v1.training import TrainingRestAdapter
from project.adapters.rest.v1.run import RunRestAdapter


os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

app = FastAPI()

app.include_router(FilesRestAdapter().router)
app.include_router(RunRestAdapter().router)
app.include_router(TrainingRestAdapter().router)
