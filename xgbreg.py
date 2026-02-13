#
# Generic regression example using XGBregressor which is the best regression machine learning algorithm
#
# To use it:
# ---------------------------------------------------
#  1. Update get_data method to fetch required data
#  2. Uncomment grid_search call in main method to identify the best parameters for XGBRegressor
#  3. After the best parameters are identified and printed, pass that as parameters to XGBRegressor instance in train_xgbr method.
#  4. Comment grid_search method and uncomment train_predict method call in main method to use

import xgboost as xgb
import pandas
from sklearn.datasets import fetch_california_housing, load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV

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

def train_xgbr (X_train, y_train):
    params = {'colsample_bytree': 0.7, 'learning_rate': 0.05, 'max_depth': 7, 'min_child_weight': 4,
              'n_estimators': 500, 'nthread': 4, 'objective': 'reg:squarederror', 'subsample': 0.7}

    xgbr = xgb.XGBRegressor(**params)
    xgbr.fit(X_train, y_train)
    return xgbr

def train_predict (X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    xgbr = train_xgbr(X_train, y_train)
    print("Score", xgbr.score(X_test, y_test))
    predictions = xgbr.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("Mean Squared Error:", mse)
    print("R-squared Score:", r2)

def get_data ():
    # Loading the California housing dataset
    data = load_diabetes(as_frame=True)
    X, y = data.data, data.target
    return X, y

if __name__ == '__main__':
    X, y = get_data()

    print("\nX:\n", X[:12].to_string())
    print("\nY:\n", y[:12].to_string())

    # Call this to find the best arguments for XGBRegressor and the pass that in line #25 in train_xgbr function
    # grid_search(xgb.XGBRegressor(), X, y)

    # Call this to do the training on data and prediction
    train_predict (X, y)