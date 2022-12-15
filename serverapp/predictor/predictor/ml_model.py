import re

import pandas as pd
from joblib import load
import ru_core_news_sm as ru

from predictor.config import Config

_cfg = Config()
_tfidf = load(_cfg.vectorizer_path)
_lr_clf = load(_cfg.model_path)
_lem = ru.load()


def convert(text):
    text = text.lower()
    # Delete all non-letter symbols
    text = " ".join(re.sub(r'[^u"а-яА-Я"]', ' ', text).split())
    # Delete single-letter words
    text = " ".join(re.sub(r'(^|\s)\w{1}(\s\w{1})*($|\s)', ' ', text).split())

    doc = _lem(text)
    text = " ".join(token.lemma_ for token in doc)
    return text


def predict(text):
    text = convert(text)
    features = _tfidf.transform(pd.Series(text))
    return _lr_clf.predict_proba(features)[0][0]
