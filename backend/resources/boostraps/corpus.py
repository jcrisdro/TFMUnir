import nltk


def get_corpus():
    """ get corpus """
    for corpus in ['reuters', 'gutenberg', 'stopwords', 'brown']:
        nltk.download(corpus)

for corpus in ['reuters', 'gutenberg', 'stopwords', 'brown']:
    nltk.download(corpus)
