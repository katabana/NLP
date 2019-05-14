from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report
import pandas
import os
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_auc_score
from datetime import date
import sklearn.metrics as skm


def metrics(y_test, y_score):
	for f in [skm.precision_score, skm.recall_score, skm.f1_score]:
		print(f.__name__, f(y_test, y_score))



def main():
	for v in ['iv', 'iii', 'ii', 'i']:
		path = "data/{}/".format(v)
		train_dir = 'training'
		test_dir = 'testing'

		training_files = [os.listdir("{}/inne/{}".format(path, train_dir)), os.listdir("{}/zmiana/{}".format(path, train_dir))]
		test_files = [os.listdir("{}/inne/{}".format(path, test_dir)), os.listdir("{}/zmiana/{}".format(path, test_dir))]

		tr = []
		for tf in training_files[0]:
		    tr.append(os.path.join(os.path.join(path, 'inne', train_dir), tf))
		for tf in training_files[1]:
		    tr.append(os.path.join(os.path.join(path, 'zmiana', train_dir), tf))


		te = []
		for tf in test_files[0]:
		    te.append(os.path.join(os.path.join(path, 'inne', test_dir), tf))
		for tf in test_files[1]:
		    te.append(os.path.join(os.path.join(path, 'zmiana', test_dir), tf))

		# convert to feature vector
		feature_extraction = TfidfVectorizer(input='filename')
		X = feature_extraction.fit_transform(tr + te)

	   #  print(X)


		# split into training- and test set
		num_training = len(tr)
		X_train = X[:num_training]
		X_test = X[num_training:]
		y_train = [1 for _ in training_files[1]] + [0 for _ in training_files[0]]
		y_test = [1 for _ in test_files[1]] + [0 for _ in test_files[0]]


		# train classifier
		clf = LinearSVC()
		clf.fit(X_train, y_train)


		# evaluate predictions
		y_score = clf.predict(X_test)
	
		print("Variant {}".format(v))
		metrics(y_test, y_score.round())
		print()

main()
    
