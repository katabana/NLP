# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14xVE8wT6croxRtyrib1V3KO79IEHF4yl
"""

!pip install flair

import flair

from sklearn.metrics import classification_report
import pandas as pd
import os
import numpy as np
import sklearn.metrics as skm
from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path
from flair.data import Sentence
import csv


def metrics(y_test, y_score):
  s = ""
  for f in [skm.precision_score, skm.recall_score, skm.f1_score]:
    s += "{}: {}\n".format(f.__name__, f(y_test, y_score))
  return s

for v in ['i', 'ii', 'iii', 'iv']:
  os.makedirs(v, exist_ok=True)

for v in ['i']:
	
        path = "{}/".format(v)
      
        corpus = NLPTaskDataFetcher.load_classification_corpus(Path(path), test_file='test.csv', train_file='train.csv')

        word_embeddings = [WordEmbeddings('pl'), FlairEmbeddings('polish-forward'), FlairEmbeddings('polish-backward')]

        document_embeddings = DocumentLSTMEmbeddings(word_embeddings, hidden_size=512, reproject_words=True, reproject_words_dimension=256)

        clf = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=False)

        trainer = ModelTrainer(clf, corpus)

        trainer.train('path', max_epochs=5, embeddings_in_memory=False, mini_batch_size=12)
        
      

        te = []
        with open(path + 'te.txt', 'r') as ytf:
          te = eval(ytf.read())
          
        te = [Sentence(t) for t in te]

        y_score = clf.predict(te)
        y_s =[]
        for i in range(len(y_score)):
          if len(y_score[i].labels) > 0:
            y_s.append(y_score[i].labels[0].value)
          else:
            y_s.append('inne')
            

        y_score = [1 if l == 'zmiana' else 0 for l in y_s]
        y_test = []
        with open(path + 'y_test.txt', 'r') as ytf:
          y_test = eval(ytf.read())
          

        print("Variant {}".format(v))
        metrics(y_test, y_score)
        print()
        with open(path + 'result', 'w') as f:
          f.write(metrics(y_test, y_score))