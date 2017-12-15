import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
from time import time
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


def log():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger('KDD2009')
    return logger

logger = log()



############################## Split Dataset ##############################################
logger.info('Start to split data set into train set, validation set and test set randomly')

# Split X to train, validation and test
train_proportion = 0.5

def train_validate_test_split(X, Y, train_percent):
    totLen = len(X)
    train_end = int(totLen * train_percent)
    trainX = X[:train_end]
    trainY = Y[:train_end]
    testX = X[train_end:]
    testY = Y[train_end:]
    return trainX, trainY, testX, testY

trainX, trainY, testX, testY = train_validate_test_split(X, Y, train_proportion)


############################## Build Model #################################################
# Train and test your model using (trainX, trainY), (testX, testY)
def benchmark(clf, trainX, trainY, testX, testY, logger):
    clf_descr = str(clf).split('(')[0]
    logger.info('Start to fit %s' % clf_descr)
    # Train the clf, and record the training time
    t0 = time()
    clf.fit(trainX, trainY)
    train_time = time() - t0
    print('Training time: %0.3fs' % train_time)

    # Fit the clf to the test dataset, and record the testing time
    t0 = time()
    predict = clf.predict(testX)
    test_time = time() - t0
    print('Testing time: %0.3fs' % test_time)

    score = float(accuracy_score(testY, predict, normalize=False)) / len(testY)
    print('Accuracy of {0}: {1:.2%}'.format(clf_descr, score))

    logger.info('Finished fitting %s' % clf_descr +'\n')
    return clf_descr, score, train_time, test_time

def drawModelComparison(results):
    indices = np.arange(len(results))
    results = [[result[i] for result in results] for i in range(4)]
    clf, score, train_time, test_time = results

    train_time = np.array(train_time) / np.max(train_time)
    test_time = np.array(test_time) / np.max(test_time)

    plt.figure(figsize=(12, 8))
    plt.title("Model Comparison for bigdata")
    plt.barh(indices, score, .2, label="score", color='navy')
    plt.barh(indices + .3, train_time, .2, label="training time",
             color='c')
    plt.barh(indices + .6, test_time, .2, label="test time", color='darkorange')
    plt.yticks(())
    plt.legend(loc='best')
    plt.subplots_adjust(left=.25)
    plt.subplots_adjust(top=.95)
    plt.subplots_adjust(bottom=.05)

    for i, c in zip(indices, clf):
        plt.text(-.3, i, c)

    plt.savefig('Model_Comparison bigdata.png')

# Gaussian Naive Bayes
gnb = GaussianNB()

# Logistic Regression
lr = LogisticRegression(C=10, solver='sag', tol=0.1)

# Random Forest Classifier
rfc = RandomForestClassifier(max_depth=15, n_estimators=10)

#Adaboosting classifier
AdaDT = AdaBoostClassifier(DecisionTreeClassifier(max_depth=8),n_estimators=10,learning_rate=0.5)

# Bagging classifier
bagging_lr = BaggingClassifier(LogisticRegression(C=10, solver='sag', tol=0.1))

# Result
results = []
for clf, name in ((gnb, 'Gaussian Naive Bayes'),
                  (lr, 'Logistic Regression'),
                  (rfc, 'Random Forest'),
                  (AdaDT, 'Adaboosting classifier'),
                  # (svc, 'SVM  classifier'),
                  (bagging_lr, 'Bagging')):
    results.append(benchmark(clf, trainX, trainY, testX, testY, logger))

drawModelComparison(results)

y_test = []
y_score = []

def ROCplot(classifier):
    y_score = classifier.fit(trainX, trainY).predict_proba(testX)
    y_test = classifier.fit(trainX, trainY).predict_proba(testX)
    # y_test = testY.as_matrix()
    # y_test[y_test == '0'] = 0
    # y_test[y_test == '1'] = 1
    # y_test[y_test == '2'] = 2
    # y_test = y_test.T
    return y_test, y_score

for classifier in (gnb,lr,rfc,AdaDT,bagging_lr):
    y_test.append(ROCplot(classifier)[0])
    y_score.append(ROCplot(classifier)[1])

def draw_roc(ytest, yscore):
    plt.figure()
    label = ['gnb','lr','rfc','AdaDT','bagging']
    color = ['red', 'navy', 'yellow', 'aqua', 'darkorange']
    for i in range(len(ytest)):
        y_test = ytest[i]
        y_score = yscore[i]
        fpr, tpr, _ = roc_curve(y_test, y_score[:, 1])
        roc_auc = auc(fpr, tpr)
        lw = 2
        plt.plot(fpr, tpr, color=color[i],
             lw=lw, label= label[i]+' ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC bigdata')
        plt.legend(loc="lower right")
    plt.savefig('ROC bigdata.png')

draw_roc(y_test, y_score)