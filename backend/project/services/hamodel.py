import base64
import hashlib
import shutil
import os
import mimetypes
import time
import pandas as pd

from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
from gensim.models import Word2Vec
from nltk.corpus import stopwords, brown, reuters, gutenberg
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances

from project.services.explode import ExplodeService
from project.clients.aws import AWSClient
from constants import ROOT_PROJECT, PATH_DIRECTORY


class HAModelService:
    """ training model adapter """

    def __init__(
            self, type_model: str = None, corpus: str = 'brown', transformer: str = 'paraphrase-MiniLM-L6-v2',
            resource_video: str = 'local') -> None:
        self.type_model = type_model
        self.model = None
        self.corpus = corpus
        self.transformer = transformer
        self.explode_service = ExplodeService()
        self.aws_cliente = AWSClient()
        self.df_embeddings = None
        self.__start_time = time.time()
        self.__metrics = {}
        self.resource_video = resource_video
        print(f"HAModelService started [{type_model} {corpus} {transformer} {resource_video}]")

    def __del__(self) -> None:
        print("HAModelService stopped")

    def __set_time__(self, start_time: float = 0.0):
        """ set time """
        self.__start_time = start_time

    def __get_time__(self, method: str = None):
        """ get time """
        self.__metrics[f'{method}_time'] = "{:.6f}".format(time.time() - self.__start_time)

    def __get_metrics__(self):
        """ get metrics """
        return self.__metrics

    def __set_metrics__(self, metrics: dict = None):
        """ set metrics """
        self.__metrics = metrics

    def get_df_embeddings(self) -> None:
        """ get df embeddings """
        if self.df_embeddings is None:
            self.df_embeddings = pd.read_hdf(f'{ROOT_PROJECT}/resources/how2sign/how2sign_realigned.h5', 'df')
        self.__get_time__(method='load_embeddings')

    def get_corpus(self, corpus: str = 'brown'):
        """ return corpus """
        if corpus == 'reuters':
            return reuters.sents()
        elif corpus == 'gutenberg':
            return gutenberg.sents()
        elif corpus == 'stopwords':
            return stopwords.words('english')
        else:
            return brown.sents()

    def get_encode_video(self, video_name: str = None) -> str:
        """ get encode video """
        def __get_video__(video_name):
            self.__metrics['resource_video'] = self.resource_video
            if self.resource_video == 'aws':
                file_directory = self.aws_cliente.get_video(file_object=f"{video_name}.mp4")
                if file_directory:
                    with open(file_directory, 'rb') as video:
                        output = base64.b64encode(video.read()).decode('utf-8')
            elif self.resource_video == 'local':
                file_directory = f"{ROOT_PROJECT}/uploads/how2sign/videos/{video_name}.mp4"
                with open(file_directory, 'rb') as video:
                    output = base64.b64encode(video.read()).decode('utf-8')
            else:
                output = None
            return output

        output = __get_video__(video_name=video_name)
        if output is None:
            video_name = "_-adcxjm1R4_0-8-rgb_front"
            output = __get_video__(video_name=video_name)

        try:
            file_directory = f"{ROOT_PROJECT}/{video_name}.mp4"
            if os.path.exists(file_directory):
                os.remove(file_directory)
                print(f"File {file_directory} removed")
        except Exception as e:
            print(f"File {file_directory} can't removed {e}")
        return output

    def build_model(
            self, vector_size: int = 100, window: int = 5, min_count: int = 1, workers: int = 4):
        """ build model """
        if self.model is None:
            sentences = self.get_corpus(corpus=self.corpus)

            if self.type_model == 'semantic':
                if Path(f'resources/models/model_{self.corpus}.model').exists():
                    model = SentenceTransformer(f'resources/models/model_{self.corpus}.model')
                else:
                    model = SentenceTransformer(self.transformer)
                    model.save(f'resources/models/model_{self.corpus}.model')
            else:
                if Path(f'resources/models/model_w2v_{self.corpus}.model').exists():
                    model = Word2Vec.load(f'resources/models/model_w2v_{self.corpus}.model')
                else:
                    model = Word2Vec(
                        sentences=sentences, vector_size=vector_size, window=window, min_count=min_count,
                        workers=workers)
                    model.save(f'resources/models/model_w2v_{self.corpus}.model')
            self.model = model
        return self.model

    def distance(self, distance, rows, model):
        """ distance """
        if distance == 'cosine':
            output = cosine_distances(rows, [model])
        else:
            output = euclidean_distances(rows, [model])
        self.__get_time__(method='distance')
        return output

    def trainning(self, train: str = "test"):
        """ trainning """
        model = self.build_model()
        df_embeddings = pd.read_csv(f'resources/how2sign/how2sign_realigned_{train}.csv', sep='\t', header=0)
        df_embeddings['EMBEDDINGS_SENTENCE'] = df_embeddings['SENTENCE'].apply(lambda x: model.encode(x))
        df_embeddings.to_hdf('resources/how2sign/how2sign_realigned.h5', key='df', mode='w')
        return {
            'train': train,
            'length': len(df_embeddings),
            'model': self.type_model,
            'corpus': self.corpus,
            'transformer': self.transformer,
            'file': 'resources/how2sign/how2sign_realigned.h5'
        }

    def predict(self, sentence: str = None, distance: str = 'cosine'):
        """ predict """
        self.get_df_embeddings()
        model = self.build_model()
        if self.type_model == 'semantic':
            # validate with semantic model
            model_embeddings = model.encode(sentence)
            try:
                self.df_embeddings['EMBEDDINGS_DISTANCES'] = self.distance(
                    distance=distance, rows=self.df_embeddings['EMBEDDINGS_SENTENCE'].tolist(), model=model_embeddings)
            except Exception as e:
                print(f"Exception: {e}")
            row = self.df_embeddings.loc[self.df_embeddings['EMBEDDINGS_DISTANCES'].idxmin()]
        else:
            # TODO: mejorar la validacion de busquedas difusas
            try:
                model_embeddings = model.wv.most_similar('disclosed')
                self.df_embeddings['EMBEDDINGS_DISTANCES'] = self.distance(
                    distance=distance, rows=self.df_embeddings['EMBEDDINGS_SENTENCE'].tolist(), model=model_embeddings)
                print(f">>> Model embeddings: {model_embeddings}")
            except Exception as e:
                print(f"Exception: {e}")

        # set metrics
        self.__metrics['sentence_method'] = hashlib.md5(sentence.encode('utf')).hexdigest()
        self.__get_time__(method='predict')
        self.__metrics['distance_method'] = distance
        self.__metrics['distance_value'] = "{:.6f}".format(row['EMBEDDINGS_DISTANCES'])

        return {
            'VIDEO_ID': row['VIDEO_ID'],
            'VIDEO_PATH': self.get_encode_video(row['SENTENCE_NAME']),
            'SENTENCE_INPUT': sentence,
            'SENTENCE_OUTPUT': row['SENTENCE'],
            'EMBEDDINGS_DISTANCES': row['EMBEDDINGS_DISTANCES'].astype(float),
            }

    def load(self, file: object = None, path: str = None):
        """ load """
        now = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        try:
            if file:
                file_path = PATH_DIRECTORY / f"{now}.{file.filename.split('.')[-1]}"
                with file_path.open("wb") as fp:
                    shutil.copyfileobj(file.file, fp)
                    fp.write(file.file.read())
            elif path:
                file_path = PATH_DIRECTORY / f"{now}.{path.split('.')[-1]}"
                shutil.copy2(path, file_path)

            attr_file = {
                'path': path, 'file_size': os.path.getsize(file_path),
                'content_type': mimetypes.guess_type(file_path)
                }

            response = self.explode_service.split(ROOT_PROJECT, str(file_path), now)
            return attr_file | response
        except Exception as e:
            return f"Exception: {e}"
