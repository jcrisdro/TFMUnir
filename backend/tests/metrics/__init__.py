import pandas as pd

from os.path import exists

from constants import ROOT_PROJECT

TESTING_HAMODEL = [
    ["semantic", "brown", "cosine", "all-MiniLM-L6-v2"],
    ["semantic", "brown", "cosine", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "brown", "cosine", "paraphrase-distilroberta-base-v1"],
    ["semantic", "brown", "cosine", "paraphrase-TinyBERT-L6-v2"],
    ["semantic", "brown", "euclidean", "all-MiniLM-L6-v2"],
    ["semantic", "brown", "euclidean", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "brown", "euclidean", "paraphrase-distilroberta-base-v1"],
    ["semantic", "brown", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    ["semantic", "reuters", "cosine", "all-MiniLM-L6-v2"],
    ["semantic", "reuters", "cosine", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "reuters", "cosine", "paraphrase-distilroberta-base-v1"],
    ["semantic", "reuters", "cosine", "paraphrase-TinyBERT-L6-v2"],
    ["semantic", "reuters", "euclidean", "all-MiniLM-L6-v2"],
    ["semantic", "reuters", "euclidean", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "reuters", "euclidean", "paraphrase-distilroberta-base-v1"],
    ["semantic", "reuters", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    ["semantic", "gutenberg", "cosine", "all-MiniLM-L6-v2"],
    ["semantic", "gutenberg", "cosine", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "gutenberg", "cosine", "paraphrase-distilroberta-base-v1"],
    ["semantic", "gutenberg", "cosine", "paraphrase-TinyBERT-L6-v2"],
    ["semantic", "gutenberg", "euclidean", "all-MiniLM-L6-v2"],
    ["semantic", "gutenberg", "euclidean", "paraphrase-MiniLM-L6-v2"],
    ["semantic", "gutenberg", "euclidean", "paraphrase-distilroberta-base-v1"],
    ["semantic", "gutenberg", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    # ["semantic", "stopwords", "cosine", "all-MiniLM-L6-v2"],
    # ["semantic", "stopwords", "cosine", "paraphrase-MiniLM-L6-v2"],
    # ["semantic", "stopwords", "cosine", "paraphrase-distilroberta-base-v1"],
    # ["semantic", "stopwords", "cosine", "paraphrase-TinyBERT-L6-v2"],
    # ["semantic", "stopwords", "euclidean", "all-MiniLM-L6-v2"],
    # ["semantic", "stopwords", "euclidean", "paraphrase-MiniLM-L6-v2"],
    # ["semantic", "stopwords", "euclidean", "paraphrase-distilroberta-base-v1"],
    # ["semantic", "stopwords", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "brown", "cosine", "all-MiniLM-L6-v2"],
    # ["fuzzy", "brown", "cosine", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "brown", "cosine", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "brown", "cosine", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "brown", "euclidean", "all-MiniLM-L6-v2"],
    # ["fuzzy", "brown", "euclidean", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "brown", "euclidean", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "brown", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "reuters", "cosine", "all-MiniLM-L6-v2"],
    # ["fuzzy", "reuters", "cosine", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "reuters", "cosine", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "reuters", "cosine", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "reuters", "euclidean", "all-MiniLM-L6-v2"],
    # ["fuzzy", "reuters", "euclidean", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "reuters", "euclidean", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "reuters", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "gutenberg", "cosine", "all-MiniLM-L6-v2"],
    # ["fuzzy", "gutenberg", "cosine", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "gutenberg", "cosine", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "gutenberg", "cosine", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "gutenberg", "euclidean", "all-MiniLM-L6-v2"],
    # ["fuzzy", "gutenberg", "euclidean", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "gutenberg", "euclidean", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "gutenberg", "euclidean", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "stopwords", "cosine", "all-MiniLM-L6-v2"],
    # ["fuzzy", "stopwords", "cosine", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "stopwords", "cosine", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "stopwords", "cosine", "paraphrase-TinyBERT-L6-v2"],
    # ["fuzzy", "stopwords", "euclidean", "all-MiniLM-L6-v2"],
    # ["fuzzy", "stopwords", "euclidean", "paraphrase-MiniLM-L6-v2"],
    # ["fuzzy", "stopwords", "euclidean", "paraphrase-distilroberta-base-v1"],
    # ["fuzzy", "stopwords", "euclidean", "paraphrase-TinyBERT-L6-v2"],
]
TESTING_SENTENCES = [
    {"phrase": "Hi!", "alternative": None},
    {"phrase": "This harness; it's not comfortable, but it does serve purpose.", "alternative": None}, # noqa E501
    {"phrase": "Hi", "alternative": "Hello"},
    {"phrase": "How are you?", "alternative": "Hows it going?"},
    {"phrase": "So what they do is they ask their Chinese counterpart to produce a tea that's made the way they do.", "alternative": None}, # noqa E501
    {"phrase": "Good", "alternative": "Great"},
    {"phrase": "Do you have a lot of snow?", "alternative": "Have you gotten a lot of snow?"},
    {"phrase": "It'll shut off the computer.", "alternative": "It will power down the computer."},
    {"phrase": "Oh!", "alternative": "OMG!"},
    {"phrase": "Keep it simple stupid.", "alternative": "Less is more"},
    {"phrase": "Thank you so much.", "alternative": "I really appreciate it."},
    {"phrase": "Now we'll talk about your legs.", "alternative": "Next, let's discuss your legs."},
    {"phrase": "This is a professional window washing bucket.", "alternative": None},
    {"phrase": "Then the wrist is going to drop.", "alternative": "At this point, the wrist will dip."}, # noqa E501
    {"phrase": "And we'll mix this up real good.", "alternative": None},
    {"phrase": "Look at that.", "alternative": "Watch that."},
    {"phrase": "Using the Tailor kit will be the best way to tell our needs of our pool.", "alternative": "The best way to express our pool requirements is by using the Tailor kit"}, # noqa E501
    {"phrase": "From the side, back and forth.", "alternative": "Side to side, to and fro"},
    {"phrase": "Okay?", "alternative": "Alright?"},
    {"phrase": "Of course, we've got herbal muscle relaxants.", "alternative": "Indeed, herbal muscle relaxants are available."}, # noqa E501
    {"phrase": "You have two choices.", "alternative": None},
    {"phrase": "Good reasons for conflicts are, you're having a baby, you're getting married, there's a financial hardship at the time, you have your own business, you're the only one operating the business, if you're not there the business doesn't operate, thus you don't get paid, thus creating the financial hardship, and so forth and so on.", "alternative": None}, # noqa E501
    {"phrase": "Silicone is a breathable barrier for the skin, so it's going to allow oxygen in and out of the follicles, so it will not clog the pores and it also will prevent breakouts.", "alternative": ""}, # noqa E501
    {"phrase": "They do understand.", "alternative": "They realize."},
    {"phrase": "Here is our tattoo machine.", "alternative": None},
    {"phrase": "Let's pick it up.", "alternative": "Let's increase the speed."},
    {"phrase": "What's the purpose of the jeans?", "alternative": None},
    {"phrase": "This diamond is D in color.", "alternative": None},
    {"phrase": "Let's watch Luis as he takes a shot.", "alternative": None},
    {"phrase": "Ji!", "error": True},
    {"phrase": "How're ya?", "error": True},
    {"phrase": "Goof", "error": True},
    {"phrase": "Do ya have a lot of snow", "error": True},
    {"phrase": "It will shutoff the PC.", "error": True},
    {"phrase": "ho!", "error": True},
    {"phrase": "Keepit simple stupid.", "error": True},
]


def read_excel():
    file_test = f"{ROOT_PROJECT}/tests/metrics/BookTest.xlsx"
    if exists(file_test):
        response = {}
        for sheet in ["Error", "Sinonimos", "Numeros"]:
            df = pd.read_excel(file_test, sheet_name=sheet)
            response[sheet] = df
        return response
    return None
