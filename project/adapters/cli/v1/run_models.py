from genericpath import isfile
from multiprocessing.util import is_exiting
from project.services.hamodel import HAModelService
from constants import HA_MODEL, ROOT_PROJECT


class RunModelsCliAdapter:
    """ training model adapter """

    def __init__(self) -> None:
        self.hamodel_service = HAModelService(
            type_model=HA_MODEL['type'], corpus=HA_MODEL['corpus'], transformer=HA_MODEL['transformer'],
            distance=HA_MODEL['distance'])

    def hamodel(self, sentences: str = None, path: str = None):
        """ hearing aid model """
        print(path)
        if path and isfile(path):
            output = self.hamodel_service.load(path=path)
            print([self.hamodel_service.predict(sentence=sentences, distance='cosine') 
                   for sentences in output.get('transcription', [])])
        else:
            print(self.hamodel_service.predict(sentence=sentences, distance='cosine'))

    def vsmodel(self):
        """ visual support model """
        print("vsmodel")
