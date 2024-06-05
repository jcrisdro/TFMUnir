import shutil
import os
import mimetypes
import gensim, nltk
import pandas as pd

from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer
from gensim.models import Word2Vec
from nltk.corpus import stopwords, brown, reuters, gutenberg
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances

from project.services.explode import ExplodeService
from constants import ROOT_PROJECT, PATH_DIRECTORY


class HAModelService:
    """ training model adapter """

    def __init__(
            self, type_model: str = None, corpus: str = None, transformer: str = None, distance: str = None) -> None:
        self.type_model = type_model
        self.sentences = self.corpus(corpus=corpus)
        self.model = self.build_model(corpus=corpus, transformer=transformer)
        self.explode_service = ExplodeService()

    def __del__(self) -> None:
        print("HAModelService stopped")

    def corpus(self, corpus: str = 'brown'):
        """ return corpus """
        if corpus == 'reuters':
            return reuters.sents()
        elif corpus == 'gutenberg':
            return gutenberg.sents()
        elif corpus == 'stopwords':
            return stopwords.sents()
        else:
            return brown.sents()

    def build_model(
            self, vector_size: int = 100, window: int = 5, min_count: int = 1, workers: int = 4, corpus: str = None,
            transformer: str = 'paraphrase-MiniLM-L6-v2'):
        """ build model """

        if Path(f'resources/models/model_{corpus}.model').exists():
            if self.type_model == 'semantic':
                model = SentenceTransformer(transformer)
            else:
                model = gensim.models.Word2Vec.load(f'resources/models/model_{corpus}.model')
        else:
            if self.type_model == 'semantic':
                model = SentenceTransformer(transformer)
            else:
                model = Word2Vec(
                    sentences=self.sentences, vector_size=vector_size, window=window, min_count=min_count,
                    workers=workers)

            model.save(f'resources/models/model_{corpus}.model')

        return model

    def distance(self, distance, row, model):
        """ distance """

        if distance == 'cosine':
            output = cosine_distances([row], [model])
            return output[0][0]
        else:
            return euclidean_distances

    def trainning(self, train: str = "test"):
        """ trainning """

        df_embeddings = pd.read_csv(f'resources/how2sign/how2sign_realigned_{train}.csv', sep='\t', header=0)
        df_embeddings['EMBEDDINGS_SENTENCE'] = df_embeddings['SENTENCE'].apply(lambda x: self.model.encode(x))
        df_embeddings.to_hdf('resources/how2sign/how2sign_realigned.h5', key='df', mode='w')

    def predict(self, sentence: str = None, distance: str = 'cosine'):
        """ predict """
        df_embeddings = pd.read_hdf('resources/how2sign/how2sign_realigned.h5', 'df')
        model_embeddings = self.model.encode(sentence)

        try:
            df_embeddings['EMBEDDINGS_DISTANCES'] = df_embeddings.EMBEDDINGS_SENTENCE.apply(
                lambda x: self.distance(distance=distance, row=x, model=model_embeddings))
        except Exception as e:
            print(f"Exception: {e}")

        row = df_embeddings.loc[df_embeddings['EMBEDDINGS_DISTANCES'].idxmin()]

        return {
            'VIDEO_NAME': row['VIDEO_NAME'], 
            'SENTENCE_NAME': row['SENTENCE_NAME'], 
            'SENTENCE': row['SENTENCE'], 
            'EMBEDDINGS_DISTANCES': row['EMBEDDINGS_DISTANCES'].astype(float), 
            'START_REALIGNED': row['START_REALIGNED'],
            'END_REALIGNED': row['END_REALIGNED'], 
            'VIDEO_ID': row['VIDEO_ID']
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

            attr_file = {'path': path, 'file_size': os.path.getsize(file_path), 
                         'content_type': mimetypes.guess_type(file_path)}

            response = self.explode_service.split(ROOT_PROJECT, str(file_path), now)

            return attr_file | response
        except Exception as e:
            return f"Exception: {e}"