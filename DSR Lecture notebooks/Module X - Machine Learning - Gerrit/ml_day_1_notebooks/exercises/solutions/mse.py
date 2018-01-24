y_pred_train = least_squares.predict(X_train)
y_pred_test = least_squares.predict(X_test)

print("Train MSE: %.4f" % mean_squared_error(y_pred_train, y_train))
print("Test MSE: %.4f" % mean_squared_error(y_pred_test, y_test))