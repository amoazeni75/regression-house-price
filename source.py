# -*- coding: utf-8 -*-
"""
@author: S.Alireza Moazeni(S.A.M.P.8)
@tutorial source: Deep Learning With Python, Develop Deep Learning Models On Theano And TensorFlow Using
Keras, Jason Brownlee
"""

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# load dataset
dataframe = pandas.read_csv("housing.csv", delim_whitespace=True, header=None)
dataset = dataframe.values

# split into input (X) and output (Y) variables
X = dataset[:,0:13]
Y = dataset[:,13]

# define base mode
"""
No activation function is used for the output layer because it is a regression
problem
"""
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(13, input_dim=13, kernel_initializer= 'normal' , activation= 'relu' ))
    model.add(Dense(1, kernel_initializer= 'normal' ))
    # Compile model
    model.compile(loss= 'mean_squared_error' , optimizer= 'adam' )
    return model

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# evaluate model with standardized dataset
estimators = []
estimators.append(( 'standardize' , StandardScaler()))
estimators.append(( 'mlp' , KerasRegressor(build_fn=baseline_model, nb_epoch=50,
batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)

"""
we can use scikit-learn’s Pipeline framework to perform the standardization during the
model evaluation process, within each fold of the cross validation
"""


kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))
