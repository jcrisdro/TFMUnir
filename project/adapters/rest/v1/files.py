import shutil
import os

from pathlib import Path
from fastapi import APIRouter, UploadFile
from datetime import datetime

from constants import ROOT_PROJECT
from project.services.etl import ETL

PATH_DIRECTORY = Path("resources/uploads/")

class Files:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.etl_service = ETL()
        self.routes()
    
    def routes(self):

        @self.router.post("/v1/load")
        async def load(file: UploadFile):
            now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
            try:
                file_path = PATH_DIRECTORY / f"{now}.{file.filename.split('.')[-1]}"
                with file_path.open("wb") as fp:
                    shutil.copyfileobj(file.file, fp)
                    fp.write(file.file.read())

                frames, audio = self.etl_service.split(ROOT_PROJECT, str(file_path), now)

                return {
                    "file_path": file_path, 
                    "original_name": file.filename, 
                    "file_size": os.path.getsize(file_path), 
                    "content_type": file.content_type,
                    "frames": frames
                    }
            except Exception as e:
                return f"Exception: {e}"
