#!/usr/bin/env python
import optparse
import sys
from collections import defaultdict, Counter
import operator
from sklearn import svm,grid_search
import numpy as np
from sklearn import cross_validation

optparser = optparse.OptionParser()
optparser.add_option("-c", "--score", dest="score_train", default="data/train/es-en_score.train", help="Score train set")
optparser.add_option("-s", "--source", dest="source_train", default="data/train/es-en_source.train", help="Scourse train set")
optparser.add_option("-t", "--target", dest="target_train", default="data/train/es-en_target.train", help="Target train set")
optparser.add_option("-f", "--features", dest="feature_train", default="data/train/train_features", help="Feature train set")

# k = 11 for best result!
optparser.add_option("-k", "--k", dest="k", type="int", default=11, help="k nearest neighbors")
(opts, _) = optparser.parse_args()

score = [s.strip() for s in open(opts.score_train).readlines()]
source = [s.strip() for s in open(opts.source_train).readlines()]
target = [s.strip().split() for s in open(opts.target_train).readlines()]
features = [s.strip().split() for s in open(opts.feature_train).readlines()]

# Set the weights)
weights = {}
for i, f in enumerate(features):
    weights[i] = 1
        

def get_label(feats, clf):
    label = clf.predict(feats)
    return label[0]

# Build SVM Classifier
X = features
Y = score
parameters = {'kernel':('linear','rbf'), 'C':[1,10],'gamma':[0.0,1.0]}
svr = svm.SVC()
clf = grid_search.GridSearchCV(svr,parameters,cv=10)
# clf = svm.SVC(gamma=0.001, C=100.)

clf = clf.fit(X, Y)  

# Predict Scores
test_features = [s.strip().split() for s in open("test-data/test_features")]

test_scores = {}
for i, feats in enumerate(test_features):
    test_scores[i] = get_label(feats, clf)

for score in test_scores.values():
    sys.stdout.write("%s\n" % score)




