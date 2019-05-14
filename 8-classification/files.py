from sklearn.metrics import classification_report
import pandas
import os
import numpy as np
import sklearn.metrics as skm
import random


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
    for v in ['ii', 'i']:
	
        global path
        path = "data/{}/".format(v)
        train_dir = 'training'
        test_dir = 'testing'


        training_files = [os.listdir("{}/inne/{}".format(path, train_dir)), os.listdir("{}/zmiana/{}".format(path, train_dir))]
        test_files = [os.listdir("{}/inne/{}".format(path, test_dir)), os.listdir("{}/zmiana/{}".format(path, test_dir))]


        tr = []
        for tf in training_files[0]:
            tr += preprocess('inne', train_dir, tf)
        for tf in training_files[1]:
            tr += preprocess('zmiana', train_dir, tf)



        te = []
        y_test = []
        s0 = len(test_files[0])
        s1 = len(test_files[1])
        for tf in random.sample(test_files[0], k=s0*1//20):
            te += preprocess('inne', test_dir, tf)
            y_test.append('inne')
        for tf in random.sample(test_files[1], k=s1*1//20):
            te += preprocess('zmiana', test_dir, tf)
            y_test.append('zmiana')

		
		# reduce tr and te sizes
        tr = random.sample(tr, k=len(tr)*1//20)

        save_file(tr, "{}{}".format(path, 'train.csv'))
        save_file(te, "{}{}".format(path, 'test.csv'))


        y_test = [1 if l == 'zmiana' else 0 for l in y_test]
        with open(path + 'y_test.txt', 'w') as y_test_file:
            y_test_file.write(str(y_test))

        with open(path + 'te.txt', 'w') as fil:
            fil.write(str(te))
        
    
main()
