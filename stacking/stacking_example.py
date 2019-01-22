import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier


def run(data):
    X = np.array([i[:-1] for i in data], dtype=float)
    Y = np.array([i[-1] for i in data])

    label_encoder = LabelEncoder()
    label_encoder.fit(Y)
    Y = label_encoder.transform(Y)

    dev_cutoff = int(len(Y) * 4/5)
    X_dev = X[:dev_cutoff]
    Y_dev = Y[:dev_cutoff]
    X_test = X[dev_cutoff:]
    Y_test = Y[dev_cutoff:]

    n_trees = 10
    n_folds = 5

    clfs = [
        RandomForestClassifier(n_estimators=n_trees, criterion='gini'),
        ExtraTreesClassifier(n_estimators=n_trees * 2, criterion='gini'),
        GradientBoostingClassifier(n_estimators=n_trees)
    ]

    skf = list(StratifiedKFold(Y_dev, n_folds))

    blend_train = np.zeros((X_dev.shape[0], len(clfs)))
    blend_test = np.zeros((X_test.shape[0], len(clfs)))

    print('X_test.shape = %s' % (str(X_test.shape)))
    print('blend_train.shape = %s' % (str(blend_train.shape)))
    print('blend_test.shape = %s' % (str(blend_test.shape)))

    for j, clf in enumerate(clfs):
        print('Training classifier [%s]' % j)
        blend_test_j = np.zeros((X_test.shape[0], len(skf)))
        for i, (train_index, cv_index) in enumerate(skf):
            # print('Fold [%s]' % i)

            X_train = X_dev[train_index]
            Y_train = Y_dev[train_index]
            X_cv = X_dev[cv_index]
            Y_cv = Y_dev[cv_index]

            clf.fit(X_train, Y_train)

            blend_train[cv_index, j] = clf.predict(X_cv)
            blend_test_j[:, i] = clf.predict(X_test)
        blend_test[:, j] = blend_test_j.mean(1)

    print('Y_dev.shape = %s' % (Y_dev.shape))

    bclf = LogisticRegression()
    bclf.fit(blend_train, Y_dev)

    Y_test_predict = bclf.predict(blend_test)
    score = metrics.accuracy_score(Y_test, Y_test_predict)
    print('Accuracy = %s' % score)
    return score


if __name__ == '__main__':
    train_file = 'data.txt'
    import re
    data = [re.sub('\n', '' , line).split(' ') for line in open(train_file) ]
    # print(data)
    best_score = 0.0

    for i in range(10):
        print('Iteration [%s]' % i)
        random.shuffle(data)
        score = run(data)
        best_score = max(best_score, score)
        print()

    print("Best score = %s" % best_score)