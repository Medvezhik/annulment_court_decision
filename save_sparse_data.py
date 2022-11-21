import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


data = pd.read_csv('data_clean.csv')
data.drop('len_txt', axis=1, inplace=True)
data = data[data['target'].notna()]
data = data[data['clear_text'].notna()]
data.drop_duplicates(inplace=True)

train_df, temp_df = train_test_split(data, test_size=0.3, random_state=17)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=17)

train_data = train_df['clear_text']
validation_data = val_df['clear_text']
test_data = test_df['clear_text']

tfidf = TfidfVectorizer(ngram_range=(5, 12), max_features=80000)
tfidf.fit(train_data)
train_features = tfidf.transform(train_data)
validation_features = tfidf.transform(validation_data)
test_features = tfidf.transform(test_data)

sparse.save_npz('train_features.npz', train_features)
sparse.save_npz('validation_features.npz', validation_features)
sparse.save_npz('test_features.npz', test_features)

