from typing import Annotated
from pydantic import BaseModel
from fastapi import APIRouter, Body

from project.services.hearingaidmodel import HearingAidModelService
from project.services.visualsupportmodel import VisualSupportModelService

from constants import HA_MODEL, VS_MODEL


class HAModel(BaseModel):
    sentences: str

class RunRestAdapter:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
        self.hamodel_service = HearingAidModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'], 
            distance=HA_MODEL['distance'])
        self.vsmodel_service = VisualSupportModelService()
    
    def routes(self):

        # Hearing Aid Model
        @self.router.post("/v1/run/hamodel")
        async def hamodel(model: HAModel):
            try:
                return self.hamodel_service.predict(sentence=model.sentences)
            except Exception as e:
                return f"Exception: {e}"


        # Visual Support Model
        @self.router.post("/v1/run/vsmodel")
        async def vsmodel():
            try:
                return "run vsmodel"
            except Exception as e:
                return f"Exception: {e}"
