from sklearn.metrics import classification_report
import pandas
import os
import numpy as np
import fasttext
import sklearn.metrics as skm


def metrics(y_test, y_score):
	for f in [skm.precision_score, skm.recall_score, skm.f1_score]:
		print(f.__name__, f(y_test, y_score))


def preprocess(d, tdir, tf):
    lines = []
    p = os.path.join(os.path.join(path, d, tdir), tf)
    with open(p, 'r') as f:
        content = ''.join(list(f.read()))
        if tdir == 'training':
            lines.append("__label__{}\t{}".format(d, content))
        else:
            lines.append(content) 

    return lines


def save_file(data, path):
    with open(path, 'w') as f:
        for d in data:
            f.write(d + '\n')


def main():
    for v in ['iv', 'iii', 'ii', 'i']:
	
        global path
        path = "data/{}/".format(v)
        train_dir = 'training'
        test_dir = 'testing'

        # classifier = fasttext.supervised('data.train.txt', 'model')

        training_files = [os.listdir("{}/inne/{}".format(path, train_dir)), os.listdir("{}/zmiana/{}".format(path, train_dir))]
        test_files = [os.listdir("{}/inne/{}".format(path, test_dir)), os.listdir("{}/zmiana/{}".format(path, test_dir))]


        tr = []
        for tf in training_files[0]:
            tr += preprocess('inne', train_dir, tf)
        for tf in training_files[1]:
            tr += preprocess('zmiana', train_dir, tf)


        te = []
        y_test = []
        for tf in test_files[0]:
            te += preprocess('inne', test_dir, tf)
            y_test.append('inne')
        for tf in test_files[1]:
            te += preprocess('zmiana', test_dir, tf)
            y_test.append('zmiana')

        save_file(tr, "{}{}".format(path, 'train.txt'))
        save_file(te, "{}{}".format(path, 'test.txt'))


        clf = fasttext.supervised(path + 'train.txt', 'model')

        # print(te)

        y_score = clf.predict(te)
        y_score = [item for sublist in y_score for item in sublist]

        y_score = [1 if l == 'zmiana' else 0 for l in y_score]
        y_test = [1 if l == 'zmiana' else 0 for l in y_test]
        with open(path + 'y_test.txt', 'w') as y_test_file:
            y_test_file.write(str(y_test))

        # print(y_score)

        print("Variant {}".format(v))
        metrics(y_test, y_score)
        print()
        
    
main()
