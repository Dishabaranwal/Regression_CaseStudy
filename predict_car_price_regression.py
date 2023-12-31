# -*- coding: utf-8 -*-
"""Predict Car Price Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pFC96Keo9KttSkzld7IZN037k8EZPmKU
"""

import pandas as pd
import numpy as np
import seaborn as sns

#setting dimensions for the plot
sns.set(rc={"figure.figsize":(11.7,8.27)})

cars_data= pd.read_csv("/content/cars_sampled (1).csv")
cars_data.head()

cars= cars_data.copy()

cars.info()

cars.describe()

pd.set_option("display.float_format", lambda x: "%.3f" % x)
cars.describe()

#to display the maximum number of columns
pd.set_option("display.max_columns",500)
cars.describe()

col =["name","dateCreated","postalCode","lastSeen","dateCrawled"]
cars=cars.drop(columns=col, axis=1)

cars.drop_duplicates(keep="first", inplace= True)

cars.isnull().sum()

yearwise_count = cars["yearOfRegistration"].value_counts().sort_index()

print(sum(cars["yearOfRegistration"]>2018))
print(sum(cars["yearOfRegistration"]<1950))
sns.regplot(x= "yearOfRegistration", y= "price", scatter=True, fit_reg=False, data=cars)

price_count = cars["price"].value_counts().sort_index()
sns.distplot(cars['price'])

cars["price"].describe()

sns.boxplot(y=cars["price"])

print(sum(cars["price"]>150000))
print(sum(cars['price']<100))

power_count= cars['powerPS'].value_counts().sort_index()
sns.distplot(cars["powerPS"])

cars["powerPS"].describe()

sns.boxplot(y=cars["powerPS"])

sns.regplot(x="powerPS", y="price", data= cars, fit_reg=False, scatter=True)

print(sum(cars["powerPS"]>500))
print(sum(cars["powerPS"]<10))

cars1= cars[(cars.yearOfRegistration<=2018)&(cars.yearOfRegistration>=1950)
& (cars.price>=100)& (cars.price<=150000)
& (cars.powerPS>=10)&(cars.powerPS<=500)]

cars1["monthOfRegistration"]/=12

cars1['Age']= (2018-cars1["yearOfRegistration"])+ cars1['monthOfRegistration']
cars1["Age"]= round(cars1["Age"],2)
cars1['Age'].describe()

cars1= cars1.drop(columns=["yearOfRegistration",'monthOfRegistration'], axis=1)

sns.distplot(cars1["Age"])

sns.boxplot(y=cars1['Age'])

sns.distplot(cars1['price'])

sns.boxplot(y=cars1['price'])

sns.distplot(cars1["powerPS"])

sns.boxplot(y=cars1["powerPS"])

sns.regplot(x="Age", y='price', scatter=True, fit_reg=False, data=cars1)

sns.regplot(x="powerPS", y='price', scatter=True, fit_reg=False, data=cars1)

cars1["seller"].value_counts()

#to check proportion
pd.crosstab(cars1["seller"], columns='count', normalize=True)

sns.countplot(x="seller",data=cars1)

cars1['offerType'].value_counts()

sns.countplot(x="offerType", data=cars1)

cars1['abtest'].value_counts()

pd.crosstab(cars["abtest"],columns="count", normalize=True)

sns.countplot(x="abtest", data=cars1)

sns.boxplot(x="abtest",y="price",data=cars1)

cars1['vehicleType'].value_counts()

pd.crosstab(cars1["vehicleType"], columns="count", normalize=True)

sns.countplot(x="vehicleType",data=cars1
              )

sns.boxplot(x="vehicleType", y='price', data=cars1)

cars1['gearbox'].value_counts()

pd.crosstab(cars1['gearbox'], columns='count', normalize=True)

sns.countplot(x="gearbox", data=cars1)

sns.boxplot(x="gearbox", y="price", data=cars1)

cars1["model"].value_counts()

pd.crosstab(cars1["model"], columns="count", normalize= True)

sns.countplot(x="model", data=cars1
              )

sns.boxplot(x=cars1["model"],y=cars1['price'])

cars1["kilometer"].value_counts().sort_index()

pd.crosstab(cars1["kilometer"], columns="count", normalize= True)

sns.boxplot(x= cars1["kilometer"], y=cars['price'])

cars1['kilometer'].describe()

sns.distplot(cars1["kilometer"], bins=8, kde=False)

sns.regplot(x=cars1["kilometer"], y=cars1["price"], scatter=True, fit_reg=False)

cars1['fuelType'].value_counts()

pd.crosstab(cars1["fuelType"], columns="count", normalize=True)

sns.countplot(x="fuelType", data=cars1)

sns.boxplot(x=cars1["fuelType"], y= cars1['price'])

cars1["brand"].value_counts()

pd.crosstab(cars1["brand"], columns='count', normalize=True)

sns.countplot(x=cars1["brand"])

sns.boxplot(x=cars1["brand"], y=cars1["price"])

cars1["notRepairedDamage"].value_counts()

pd.crosstab(cars1["notRepairedDamage"], columns='count', normalize=True)

sns.countplot(x=cars1["notRepairedDamage"])

sns.boxplot(x=cars1["notRepairedDamage"], y=cars1["price"])

col= ["seller",'offerType',"abtest"]
cars1= cars1.drop(columns=col, axis=1)

cars_copy=cars1.copy()

cars_select1= cars1.select_dtypes(exclude=[object])
correlation= cars_select1.corr()
round(correlation,3)

cars_select1.corr().loc[:,'price'].abs().sort_values(ascending=False)[1:]

#Model Building With  Inputed  Data
#cars_inputed= cars1.apply(lambda x:x.fillna(x.median())if x.dtypes=="float" else x.fillna(x.value_counts().index[0]))
#cars_inputed.isnull().sum()
cars_omit = cars1.dropna(axis=0)

cars_omit= pd.get_dummies(cars_omit,drop_first=True)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

x1 = cars_omit.drop(["price"], axis="columns", inplace=False)
y1= cars_omit['price']

prices= pd.DataFrame({"1.Before": y1, "2.After":np.log(y1)})
print(prices)

prices.hist()

y1=np.log(y1)

x_train, x_test,y_train, y_test = train_test_split(x1,y1, test_size=0.3, random_state=3)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

base_pred= np.mean(y_test)
print(base_pred)

base_pred = np.repeat(base_pred, len(y_test))

base_rmse= np.sqrt(mean_squared_error(y_test, base_pred))
print(base_rmse)

lgr= LinearRegression(fit_intercept=True)

model_lin1= lgr.fit(x_train, y_train)

cars_predictions_lin1=lgr.predict(x_test)

lin_mse1= mean_squared_error(y_test, cars_predictions_lin1)
lin_rmse1= np.sqrt(lin_mse1)
print(lin_rmse1)

r2_lin_test1= model_lin1.score(x_test, y_test)
r2_lin_train1= model_lin1.score(x_train, y_train)
print(r2_lin_train1,r2_lin_test1)

residuals1 = y_test- cars_predictions_lin1
print(residuals1)

sns.regplot(x=cars_predictions_lin1, y=residuals1, scatter=True, fit_reg= False, data= cars1)

residuals1.describe()

rf = RandomForestRegressor(n_estimators= 100, max_features="auto",max_depth= 100, min_samples_split=10, min_samples_leaf=4, random_state=1)

model_rf1= rf.fit(x_train, y_train)

cars_predictions_rf1= rf.predict(x_test)

rf_mse1= mean_squared_error(y_test, cars_predictions_rf1)
rf_rmse1= np.sqrt(rf_mse1)
print(rf_rmse1)

r2_rf_test1= model_rf1.score(x_test, y_test)
r2_rf_train1= model_rf1.score(x_train, y_train)
print(r2_rf_train1, r2_rf_test1)

