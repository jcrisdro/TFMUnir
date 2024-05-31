from fastapi import APIRouter, HTTPException

from project.services.hearingaidmodel import HearingAidModelService
from project.services.visualsupportmodel import VisualSupportModelService

from constants import HA_MODEL, VS_MODEL


class TrainingRestAdapter:

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
        self.hamodel_service = HearingAidModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'], 
            distance=HA_MODEL['distance'])
        self.vsmodel_service = VisualSupportModelService()
    
    def routes(self):

        # Hearing Aid Model
        @self.router.get("/v1/training/hamodel")
        async def hamodel():
            try:
                return self.hamodel_service.trainning(train=HA_MODEL['trainning'])
            except Exception as e:
                return f"Exception: {e}"


        # Visual Support Model
        @self.router.get("/v1/training/vsmodel")
        async def vsmodel():
            try:
                return "load file"
            except Exception as e:
                return f"Exception: {e}"
