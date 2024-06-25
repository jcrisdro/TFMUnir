from fastapi import APIRouter

from project.services.hamodel import HAModelService
from constants import HA_MODEL


class TrainModelsRestAdapter:
    """ training model adapter """

    def __init__(self) -> None:
        self.router = APIRouter()
        self.routes()
        self.hamodel_service = HAModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'])

    def routes(self):
        """ routes """

        @self.router.get("/hamodel")
        async def hamodel():
            """ hearing aid model """
            try:
                return self.hamodel_service.trainning(train=HA_MODEL['trainning'])
            except Exception as e:
                return f"Exception: {e}"
