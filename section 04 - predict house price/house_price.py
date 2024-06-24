from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


boston_dataset = load_boston()
data = pd.DataFrame(data=boston_dataset.data,columns=boston_dataset.feature_names)
data['PRICE'] = boston_dataset.target

prices = np.log(data['PRICE'])
features = data.drop(['PRICE','INDUS','AGE'],axis=1)
target = pd.DataFrame(data=prices,columns=['PRICE'])

property_stats = np.zeros(shape=(1,11))
property_stats = features.mean().values.reshape(1,11)

regr = LinearRegression().fit(X=features,y=target)
predict_values = regr.predict(features)
#mse and rmse
mse_predicts = mean_squared_error(target,predict_values)
rmse_predicts = np.sqrt(mse_predicts)

def get_house_price(rooms,studet_per_class,next_river=False,high_confidence=True):
    
    """Quick
    Description of function
    rooms -- number of rooms : int
    studet_per_class : int
    high_confidence -- range of values
    
    """
    
    if(rooms==0 or studet_per_class<1):
        return 'Invalid values'
    
    property_stats[0][5] = rooms
    property_stats[0][10] = studet_per_class
    if(next_river):
        property_stats[0][3] = 1
    else:
        property_stats[0][3]=0
        
    predict_y = regr.predict(property_stats)
    upperBound=0
    lowerBound=0
    interval=0
    if(high_confidence):
        upperBound = predict_y + 2*rmse_predicts
        lowerBound = predict_y - 2*rmse_predicts
        interval=95
    else:
        upperbound = predict_y + rmse_predicts
        lowerBound = predict_y - rmse_predicts
        interval=68
        
    return predict_y[0][0],upperBound[0][0],lowerBound[0][0],interval

