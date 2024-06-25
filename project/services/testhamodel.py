import time
import pandas as pd
from constants import ROOT_PROJECT
from project.services.hamodel import HAModelService
from tests.metrics import TESTING_HAMODEL, TESTING_SENTENCES


class TestHAModelService:
    def __init__(self):
        self.hamodel_service = None

    def predict(self):
        start_time = time.time()
        metrics = []
        for model in TESTING_HAMODEL:
            self.hamodel_service = HAModelService(type_model=model[0], corpus=model[1], transformer=model[3],
                                                  resource_video='local')
            for sentence in TESTING_SENTENCES:
                self.hamodel_service.__set_metrics__(metrics={
                    'model': model[3], 'corpus': model[1], 'distance': model[2], 'transformer': model[3],
                    'sentence': sentence['phrase']})

                self.hamodel_service.__set_time__(start_time=time.time())
                self.hamodel_service.predict(sentence=sentence['phrase'], distance=model[2])
                metrics.append(self.hamodel_service.__get_metrics__())

                if sentence.get('alternative'):
                    self.hamodel_service.__set_metrics__(metrics={
                        'model': model[3], 'corpus': model[1], 'distance': model[2], 'transformer': model[3],
                        'sentence': sentence['phrase']})
                    self.hamodel_service.__set_time__(start_time=time.time())
                    self.hamodel_service.predict(sentence=sentence['alternative'], distance=model[2])
                    metrics.append(self.hamodel_service.__get_metrics__())
        df = pd.DataFrame(metrics)
        df.to_csv(f'{ROOT_PROJECT}/tests/metrics/metrics.csv', index=False, sep=';')
        print(time.time() - start_time)
