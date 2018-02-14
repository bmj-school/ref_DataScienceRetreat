import six; from six.moves import cPickle

import numpy as np
import sklearn.datasets
import sklearn.externals.joblib
import sklearn.feature_extraction.text
import sklearn.feature_selection
import sklearn.metrics
import sklearn.metrics
import sklearn.model_selection
import sklearn.multiclass
import sklearn.pipeline
import sklearn.preprocessing
import sklearn.svm

import sys

is_python_3 = sys.version_info[0] >= 3

def report(results, n_top=3):
    print('-' * 42)
    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                results['mean_test_score'][candidate],
                results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


def report_top_features_by_pval(label_encoder, feature_encoder, test_labels, feature_names, test, pval_threshold=0.05,
                                max_features=10):
    test_features = feature_encoder.transform(test.data)
    for class_index, j in zip(label_encoder.classes_, range(test_labels.shape[1])):
        binary_class_labels = test_labels[:, j].reshape(-1)
        f, pvals = sklearn.feature_selection.f_classif(
            X=test_features,
            y=binary_class_labels
        )

        feature_pvals = [(m, feature_names[idx]) for idx, m in enumerate(pvals)]
        feature_pvals = filter(lambda entry: entry[0] <= pval_threshold, feature_pvals)
        sorted_pvals = sorted(feature_pvals, key=lambda tup: tup[0])

        print('F-Test p-Value of top features for model {}:'.format(test.target_names[class_index]))
        for p_value, feature_name in sorted_pvals[:max_features]:
            print('{} - {}'.format(feature_name, p_value))


def report_top_features_by_mi(label_encoder, feature_encoder, test_labels, feature_names, test, max_features=15):
    dense_test_features = feature_encoder.transform(test.data).todense()
    for class_index, j in zip(label_encoder.classes_, range(test_labels.shape[1])):
        binary_class_labels = test_labels[:, j].reshape(-1)
        mi = sklearn.feature_selection.mutual_info_classif(
            X=dense_test_features,
            y=binary_class_labels,
            discrete_features=False
        )

        mi = sorted([(m, feature_names[idx]) for idx, m in enumerate(mi)], key=lambda tup: tup[0], reverse=True)
        print('Mutual Information of top features for model {}:'.format(test.target_names[class_index]))
        for mutual_info, feature_name in mi[:max_features]:
            print('{} - {}'.format(feature_name, mutual_info))


def get_train_test():
    train = sklearn.datasets.fetch_20newsgroups(subset='train', remove=('headers'))
    test = sklearn.datasets.fetch_20newsgroups(subset='test', remove=('headers'))
    return train, test


def model_selection(train, test, cv=3, test_size=0.33):
    """
    Run model selection with the given data and targets.
    :param data: n-element list of newsgroup posts.
    :param targets: n-element list of newgroups label.
    :param target_names: textual description of newsgroup labels.
    :return: cross validated classification pipeline, label encoder.
    """
    pipeline = sklearn.pipeline.Pipeline(
        [
            ('vectorizer', sklearn.feature_extraction.text.TfidfVectorizer(stop_words='english')),
            ('clf', sklearn.multiclass.OneVsRestClassifier(sklearn.svm.LinearSVC()))
        ]
    )

    parameters = {
        'clf__estimator__C': [1e-1, 1e0, 1e1],
        # 'clf__estimator__dual': [False],
        # 'clf__estimator__loss': ['hinge'],
        # 'clf__estimator__penalty': ['l1', 'l2'],
        # 'vectorizer__max_features': [1024, 2048],
        # 'vectorizer__ngram_range': [(1, 2), (1, 3), (2, 2)]
    }

    # validation data
    data_train, data_val, labels_train, labels_val = sklearn.model_selection.train_test_split(
        train.data,
        train.target,
        test_size=test_size,
        random_state=42
    )

    label_encoder = sklearn.preprocessing.LabelBinarizer().fit(labels_train)
    clf = sklearn.model_selection.GridSearchCV(
        pipeline,
        parameters,
        scoring='average_precision',
        refit=True,
        cv=cv,
        n_jobs=-1,
        verbose=2
    )
    clf.fit(data_train, label_encoder.transform(labels_train))

    best_pipeline = clf.best_estimator_
    best_tfidf = best_pipeline.steps[0][1]
    best_clf = best_pipeline.steps[1][1]

    predictions_val = best_pipeline.predict(data_val)
    classif_report = sklearn.metrics.classification_report(
        label_encoder.transform(labels_val),
        predictions_val,
        target_names=train.target_names
    )

    report(clf.cv_results_)

    print('-' * 42)
    print('validation data classification report')
    print('-' * 42)
    print(classif_report)

    predictions_test = best_pipeline.predict(test.data)
    classif_report = sklearn.metrics.classification_report(
        label_encoder.transform(test.target),
        predictions_test,
        target_names=test.target_names
    )

    print('-' * 42)
    print('test data classification report')
    print('-' * 42)
    print(classif_report)

    # feature index -> feature name
    if is_python_3:
        feature_names = {v: k for k, v in best_tfidf.vocabulary_.items()}
    else:
        feature_names = {v: k for k, v in best_tfidf.vocabulary_.iteritems()}

    # bottom k and top k feature weights per model
    k = 2
    for model, model_name in zip(best_clf.coef_, test.target_names):
        model_coefs = []
        for idx, feature_weight in enumerate(model):
            model_coefs.append((feature_names[idx], feature_weight))
        model_coefs_sorted = sorted(model_coefs, key=lambda tup: tup[1])
        print(model_name)
        print(model_coefs_sorted[:k] + model_coefs_sorted[-k:])

    # report_top_features_by_mi(label_encoder, best_tfidf, label_encoder.transform(test.target), feature_names, test)
    report_top_features_by_pval(label_encoder, best_tfidf, label_encoder.transform(test.target), feature_names, test)

    return best_pipeline, label_encoder


if __name__ == "__main__":
    train, test = get_train_test()
    best_pipeline, label_encoder = model_selection(
        train,
        test,
        cv=2,
        test_size=0.33
    )

    # persistence
    print()
    print('saving model and encoder...')
    sklearn.externals.joblib.dump(best_pipeline, 'pipeline.pkl')
    sklearn.externals.joblib.dump(label_encoder, 'label_encoder.pkl')
    cPickle.dump(train.target_names, open('train_target_names.pkl', 'wb'))
    print('done.')
