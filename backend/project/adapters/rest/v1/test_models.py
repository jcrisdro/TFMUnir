from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter

from project.services.testhamodel import TestHAModelService


class ResponseModel(BaseModel):
    """ hamodel model """
    model: Optional[str] = None
    peticion: Optional[str] = None
    duration: Optional[float] = 0.0
    distance: Optional[str] = None
    corpus: Optional[str] = None


class TestModelsRestAdapter:
    """ test model adapter """

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
        self.test_hamodel_service = TestHAModelService()

    def routes(self):
        """ routes """
        @self.router.get("/hamodel")
        async def hamodel():
            """ hearing aid model """
            return self.test_hamodel_service.predict()
