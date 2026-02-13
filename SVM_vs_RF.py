from sklearn import datasets
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from xgboost import XGBRegressor
from xgboost import plot_tree

def grid_search (xgbr, X, y):
    parameters = {'nthread': [4],  # when use hyperthread, xgboost may become slower
                  'objective': ['reg:squarederror'],
                  'learning_rate': [.03, 0.05, .07],  # so called `eta` value
                  'max_depth': [4, 5, 6, 7],
                  'min_child_weight': [4],
                  'subsample': [0.7],
                  'colsample_bytree': [0.7],
                  'n_estimators': [500]}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)    
    xgb_grid = GridSearchCV(xgbr, parameters, cv = 2, n_jobs = 5, verbose=True)
    xgb_grid.fit(X_train, y_train)
    print(xgb_grid.best_score_)
    print(xgb_grid.best_params_)

def rand_forest_train(x_train, y_train, x_test, y_test):
    rfc = RandomForestRegressor(n_estimators=100)
    rfc.fit(x_train, y_train)
    print("Random Forest Regressor: ", rfc.score(x_test, y_test))
    return rfc.predict(x_test)

def xgb_train(x_train, y_train, x_test, y_test):
    rfc = XGBRegressor(n_estimators=200)
    rfc.fit(x_train, y_train)
    print("XGBoost Regressor: ", rfc.score(x_test, y_test))
    plot_tree(rfc)
    return rfc.predict(x_test)

def svm_train(x_train, y_train, x_test, y_test):
    svmc = svm.SVR(kernel='linear',C=1.2, epsilon=0.2)
    svmc.fit(x_train, y_train)
    print("SVM Regressor: ", svmc.score(x_test, y_test))
    return svmc.predict(x_test)

def xgb_train_with_grid_search(x_train, y_train, x_test, y_test):
    param = {'kernel': ('linear', 'poly', 'rbf', 'sigmoid'), 'C': [1, 5, 10], 'degree': [3, 8],
             'coef0': [0.01, 10, 0.5], 'gamma': ('auto', 'scale')}
    modelsvr = svm.SVR()
    svmc = GridSearchCV(modelsvr, param, cv=5, n_jobs = -1, verbose = 2)
    svmc.fit(x_train, y_train)
    print("SVM Regressor: ", svmc.score(x_test, y_test))
    return svmc.predict(x_test)

def main():
    data = datasets.load_diabetes()
    rs = RobustScaler()
    x_train, x_test, y_train, y_test = train_test_split(rs.fit_transform(data.data), data.target, test_size=0.3)
    y_pred = rand_forest_train(x_train, y_train, x_test, y_test)
    y_pred = xgb_train(x_train, y_train, x_test, y_test)
    y_pred = svm_train(x_train, y_train, x_test, y_test)

if __name__ == '__main__':
    main()

