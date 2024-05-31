import shutil
import os

from fastapi import APIRouter, UploadFile
from datetime import datetime

from constants import ROOT_PROJECT, PATH_DIRECTORY
from project.services.etl import ETLService

class FilesRestAdapter:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.etl_service = ETLService()
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

                response = self.etl_service.split(ROOT_PROJECT, str(file_path), now)

                return {
                    "file_path": file_path, 
                    "original_name": file.filename, 
                    "file_size": os.path.getsize(file_path), 
                    "content_type": file.content_type,
                    } | response
            except Exception as e:
                return f"Exception: {e}"
