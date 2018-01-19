from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

X_train, X_test, y_train, y_test = train_test_split(X, y)

params = {
    "criterion": ["mse", "mae"],
    "max_depth": [None, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

clf_grid = GridSearchCV(tree.DecisionTreeRegressor(random_state=42), 
                        params, 
                        scoring="neg_mean_squared_error", 
                        cv=5, 
                        n_jobs=-1,
                        verbose=1)

clf_grid.fit(X_train, y_train)
test_roc_score = clf_grid.score(X_test, y_test)

print("CV-score: %.4f, Test-score: %.4f" % (clf_grid.best_score_, test_roc_score))
print("Best model: %r" % clf_grid.best_estimator_)