from genericpath import isfile

from project.services.hamodel import HAModelService
from constants import HA_MODEL


class RunModelsCliAdapter:
    """ training model adapter """

    def __init__(self) -> None:
        self.hamodel_service = HAModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'])

    def hamodel(self, sentences: str = None, path: str = None):
        """ hearing aid model """
        if path and isfile(path):
            output = self.hamodel_service.load(path=path)
            print([self.hamodel_service.predict(sentence=sentences, distance=HA_MODEL['distance'])
                   for sentences in output.get('transcription', [])])
        else:
            print(self.hamodel_service.predict(sentence=sentences, distance=HA_MODEL['distance']))

    def vsmodel(self):
        """ visual support model """
        print("vsmodel")
