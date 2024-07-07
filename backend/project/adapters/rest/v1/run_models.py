from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File, Depends

from project.services.hamodel import HAModelService
from project.services.vsmodel import VSModelService
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
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'])
        self.vsmodel_service = VSModelService()

    def routes(self):
        """ routes """
        @self.router.post("/hamodel")
        async def hamodel(base: HAModel = Depends(), file: UploadFile = File(None)):
            """ hearing aid model """
            if file:
                try:
                    output = self.hamodel_service.load(file=file)
                    return [self.hamodel_service.predict(sentence=sentences, distance=HA_MODEL['distance'])
                            for sentences in output.get('transcription', [])]
                except Exception as e:
                    return f"Exception: {e}"
            return self.hamodel_service.predict(sentence=base.sentences)

        @self.router.post("/vsmodel")
        async def vsmodel(file: UploadFile = File(None)):
            """ visual support model """
            if file:
                try:
                    output = self.vsmodel_service.load(file=file)
                    print(f">>{output}<<")
                    df, frame = self.vsmodel_service.predict(
                        frame=self.vsmodel_service.picture_to_frame(file_dict=output))
                    return self.vsmodel_service.process(df=df, frame=frame)
                except Exception as e:
                    return f"Exception: {e}"
            return None
