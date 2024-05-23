import os

from fastapi import Depends, FastAPI

from project.adapters.rest.v1.files import Files
from project.adapters.rest.v1.training import Training
from project.adapters.rest.v1.run import Run


os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

app = FastAPI()

app.include_router(Files().router)
app.include_router(Run().router)
app.include_router(Training().router)
