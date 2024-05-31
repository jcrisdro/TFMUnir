import os
from pathlib import Path


ROOT_PROJECT = os.getcwd()
PATH_DIRECTORY = Path("resources/uploads/")

HA_MODEL = {
    'type': 'semantic', # semantic | fuzzy
    'tesauro': 'conceptnet', # wordnet | conceptnet
    'corpus': 'brown', # brown | reuters | gutenberg, stopwords
    'distance': 'cosine', # cosine | euclidean
    'transformer': 'all-MiniLM-L6-v2', # paraphrase-MiniLM-L6-v2 | paraphrase-distilroberta-base-v1 | paraphrase-TinyBERT-L6-v2 | all-MiniLM-L6-v2
    'trainning': 'train', # test | train | val
}

VS_MODEL = {
    'type': None, # None | None
}
