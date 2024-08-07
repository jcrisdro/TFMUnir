import time
import pandas as pd
from constants import ROOT_PROJECT
from project.services.hamodel import HAModelService
from tests.metrics import TESTING_HAMODEL, TESTING_SENTENCES
from tests.metrics import read_excel


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
                    'sentence': sentence['phrase'], 'alternative': True if sentence['alternative'] else False})

                self.hamodel_service.__set_time__(start_time=time.time())
                self.hamodel_service.predict(sentence=sentence['phrase'], distance=model[2])
                metrics.append(self.hamodel_service.__get_metrics__())

                if sentence.get('alternative'):
                    self.hamodel_service.__set_metrics__(metrics={
                        'model': model[3], 'corpus': model[1], 'distance': model[2], 'transformer': model[3],
                        'sentence': sentence['phrase'], 'alternative': True if sentence['alternative'] else False})
                    self.hamodel_service.__set_time__(start_time=time.time())
                    self.hamodel_service.predict(sentence=sentence['alternative'], distance=model[2])
                    metrics.append(self.hamodel_service.__get_metrics__())
        df = pd.DataFrame(metrics)
        df.to_csv(f'{ROOT_PROJECT}/tests/metrics/metrics.csv', index=False, sep=';')
        print(time.time() - start_time)

    def predict2(self):
        start_time = time.time()
        TESTING_SENTENCES_v2 = read_excel()
        metrics = []
        for key in TESTING_SENTENCES_v2:
            for model in TESTING_HAMODEL:
                self.hamodel_service = HAModelService(
                    type_model=model[0], corpus=model[1], transformer=model[3], resource_video='local')
                for row in range(len(TESTING_SENTENCES_v2[key])):
                
                    self.hamodel_service.__set_time__(start_time=time.time())
                    self.hamodel_service.__set_metrics__(metrics={
                        'model': model[3],
                        'corpus': model[1],
                        'distance': model[2],
                        'sentence': TESTING_SENTENCES_v2[key].iloc[row]['Find'],
                        'expected': TESTING_SENTENCES_v2[key].iloc[row]['Expect'],
                        'category': key
                        })

                    self.hamodel_service.predict(
                        sentence=TESTING_SENTENCES_v2[key].iloc[row]['Find'], distance=model[2])
                    metrics.append(self.hamodel_service.__get_metrics__())

        df = pd.DataFrame(metrics)
        df.to_csv(f'{ROOT_PROJECT}/tests/metrics/metrics.csv', index=False, sep='|')
        print(time.time() - start_time)
