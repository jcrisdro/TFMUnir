import base64
import shutil
import os
import mimetypes
import gensim
import nltk
import pandas as pd

from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
from gensim.models import Word2Vec
from nltk.corpus import stopwords, brown, reuters, gutenberg
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances

from project.services.explode import ExplodeService
from constants import ROOT_PROJECT, PATH_DIRECTORY, HOW2SIGN_DIRECTORY


class HAModelService:
    """ training model adapter """

    def __init__(
            self, type_model: str = None, corpus: str = 'brown', transformer: str = 'paraphrase-MiniLM-L6-v2') -> None:
        self.type_model = type_model
        self.model = None
        self.corpus = corpus
        self.transformer = transformer
        self.explode_service = ExplodeService()

    def __del__(self) -> None:
        print("HAModelService stopped")

    def get_corpus(self, corpus: str = 'brown'):
        """ return corpus """
        if corpus == 'reuters':
            return reuters.sents()
        elif corpus == 'gutenberg':
            return gutenberg.sents()
        elif corpus == 'stopwords':
            return stopwords.sents()
        else:
            return brown.sents()

    def get_encode_video(self, video_name: str = None) -> str:
        """ get encode video """
        try:
            with open(f'{ROOT_PROJECT}/{HOW2SIGN_DIRECTORY}/{video_name}.mp4', 'rb') as video:
                output = base64.b64encode(video.read()).decode('utf-8')
        except Exception as e:
            print(f"Exception: {e}")
            with open(f'{ROOT_PROJECT}/{HOW2SIGN_DIRECTORY}/_-adcxjm1R4_0-8-rgb_front.mp4', 'rb') as video:
                output = base64.b64encode(video.read()).decode('utf-8')
        return output

    def build_model(
            self, vector_size: int = 100, window: int = 5, min_count: int = 1, workers: int = 4):
        """ build model """
        if self.model is None:
            sentences = self.get_corpus(corpus=self.corpus)
            if Path(f'resources/models/model_{self.corpus}.model').exists():
                if self.type_model == 'semantic':
                    model = SentenceTransformer(f'resources/models/model_{self.corpus}.model')
                else:
                    model = gensim.models.Word2Vec.load(f'resources/models/model_{self.corpus}.model')
            else:
                if self.type_model == 'semantic':
                    model = SentenceTransformer(self.transformer)
                else:
                    model = Word2Vec(
                        sentences=sentences, vector_size=vector_size, window=window, min_count=min_count,
                        workers=workers)
                model.save(f'resources/models/model_{self.corpus}.model')
            self.model = model
        return self.model

    def distance(self, distance, rows, model):
        """ distance """
        if distance == 'cosine':
            return cosine_distances(rows, [model])
        else:
            return euclidean_distances

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
        model = self.build_model()
        df_embeddings = pd.read_hdf('resources/how2sign/how2sign_realigned.h5', 'df')
        model_embeddings = model.encode(sentence)
        try:
            df_embeddings['EMBEDDINGS_DISTANCES'] = self.distance(
                distance=distance, rows=df_embeddings['EMBEDDINGS_SENTENCE'].tolist(), model=model_embeddings)
        except Exception as e:
            print(f"Exception: {e}")
        row = df_embeddings.loc[df_embeddings['EMBEDDINGS_DISTANCES'].idxmin()]
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
