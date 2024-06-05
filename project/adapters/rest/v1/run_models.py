from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Depends

from project.services.hamodel import HAModelService
from constants import HA_MODEL


class HAModel(BaseModel):
    """ hamodel model """
    sentences: Optional[str] = None


class RunModelsRestAdapter:
    """ training model adapter """

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
        self.hamodel_service = HAModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'],
            distance=HA_MODEL['distance'])

    def routes(self):
        """ routes """

        @self.router.post("/hamodel")
        async def hamodel(base: HAModel = Depends(), file: UploadFile = File(None)):
            """ hearing aid model """
            if file:
                try:
                    output = self.hamodel_service.load(file=file)
                    return [self.hamodel_service.predict(sentence=sentences) 
                            for sentences in output.get('transcription', [])]
                except Exception as e:
                    return f"Exception: {e}"
            return self.hamodel_service.predict(sentence=base.sentences)

        @self.router.post("/vsmodel")
        async def vsmodel():
            """ visual support model """
            print("vsmodel")
