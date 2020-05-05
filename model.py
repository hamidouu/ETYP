# Decision Tree Regression

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import joblib

# Importing the dataset
dataset = pd.read_csv('house_data.csv')
dataset['price'] = dataset['price'].str.replace(' ', '').astype(float)

#Splitting the dataset into the features set and  set
X2 = dataset.iloc[:, 4:6].values
x1 = dataset.iloc[:, 2:3].values
X = np.concatenate((x1, X2), axis=1)

y = dataset.iloc[:, -1].values


#missing data
"""
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = "NaN", strategy = 'mean', axis = 0)
imputer = imputer.fit(X[:, 2:3])
X[:, 2:3] = imputer.transform(X[:, 2:3])
"""
#Categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train[:,57:] = sc_X.fit_transform(X_train[:,58:])
X_test[:,57:] = sc_X.fit_transform(X_test[:,58:])

from sklearn.linear_model import Ridge
ridge_reg = Ridge(alpha=0.6, solver="cholesky")
ridge_reg.fit(X_train, y_train)
# Saving model to disk
pickle.dump(ridge_reg, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
joblib.dump(sc_X, "data_transformer.joblib")
#ridge_reg.save("price_prediction_model.h5")
