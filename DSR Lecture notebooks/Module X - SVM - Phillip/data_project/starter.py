import sklearn.datasets
import sklearn.feature_extraction.text
import sklearn.metrics
import sklearn.multiclass
import sklearn.svm

import numpy as np

#print(np.__version__)
#raise

def get_train_test():
    train = sklearn.datasets.fetch_20newsgroups(subset='train', remove=('headers'))
    test = sklearn.datasets.fetch_20newsgroups(subset='test', remove=('headers'))
    return train, test


# get the training and test data
train, test = get_train_test()

# text to vector encoder with maximally 1024 dimensions
vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(max_features=1024, stop_words='english')
# newgroup (target) to multi-class label
label_encoder = sklearn.preprocessing.LabelBinarizer()

# linear svc one vs rest classifier
clf = sklearn.multiclass.OneVsRestClassifier(sklearn.svm.LinearSVC())

# encode emails in design matrix
X = vectorizer.fit_transform(train.data)
# encode email newgroups in target matrix
y = label_encoder.fit_transform(train.target)

print(X.shape, y.shape)

# fit soft-margin linear svms to X, y
clf.fit(X, y)

# generate a classification report for the test data
classif_report = sklearn.metrics.classification_report(
    label_encoder.transform(test.target),
    clf.predict(vectorizer.transform(test.data)),
    target_names=train.target_names
)

print("Test-data classification report")
print(classif_report)

test_acc = sklearn.metrics.accuracy_score(
    label_encoder.transform(test.target),
    clf.predict(vectorizer.transform(test.data))
)

print("Test-data overall accuracy", test_acc)