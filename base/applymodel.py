import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd

def apply_model(request, data, model):
    #document = request.session['document']
    columnx = request.session['column-x']
    columny = request.session['column-y']
    #model = request.session['model']


    # Label encoding for string columns
    #if model == 'Logistic Regression' or model == 'KNN' or model == 'Random Forest':
        # pass
        # for col in columnx:
        #     if type(data[col][0]) == str:
        #         data[col] = LabelEncoder().fit_transform(data[col])

    X = data[columnx]
    y = data[columny]
    df = pd.merge(X,y, left_index = True, right_index=True)
    #print(df)

    #print(X)
    #print(y)
    #print(np.array(X))
    
    # Default linear regression
    mdl = LinearRegression()

    #X_train, X_test, y_train, y_test = train_test_split(np.array(X), np.array(y), test_size=0.2)
    enc = None
    if model == 'Linear Regression':
        mdl = LinearRegression()
        df1 = df.select_dtypes(exclude = ['object'])
        df2 = df.select_dtypes(include = ['object'])
        # if not df2.empty:
        #     enc = OneHotEncoder(handle_unknown='ignore')
        #     enc.fit(df2)
        #     enc.get_feature_names_out(df2.columns)
        #     enc
        print(columny)
        dum = pd.get_dummies(df2)
        data = pd.concat([df1,dum],axis=1)
        print(data)
        data_train = data.drop(columns=columny)
        request.session['temp_col'] = list(data_train.columns)

        #X_train, X_test, y_train, y_test = train_test_split(np.array(X), np.array(y), test_size=0.2)
        X_train, X_test, y_train, y_test = train_test_split(data_train, data[columny], test_size=0.2)
        mdl.fit(X_train, y_train)
        # print(list(request.session['temp_col']))
        print("lr")
    elif model == 'Logistic Regression':
        mdl = LogisticRegression()
        
        X_train, X_test, y_train, y_test = train_test_split(data[columnx], data[columny], test_size=0.2)
        enc = OneHotEncoder(handle_unknown='ignore')
        X_train_new = enc.fit_transform(X_train).toarray()
        X_test_new = enc.transform(X_test).toarray()
        print(X_train_new, 'asdf')
        mdl.fit(X_train_new, y_train)
        print("logr")
    elif model == 'KNN':
        mdl = KNeighborsClassifier()
        X_train, X_test, y_train, y_test = train_test_split(data[columnx], data[columny], test_size=0.2)
        enc = OneHotEncoder(handle_unknown='ignore')
        X_train_new = enc.fit_transform(X_train).toarray()
        X_test_new = enc.transform(X_test).toarray()
        mdl.fit(X_train_new, y_train)
        print("knn")
    elif model == 'Random Forest':
        mdl = RandomForestClassifier()
        X_train, X_test, y_train, y_test = train_test_split(data[columnx], data[columny], test_size=0.2)
        enc = OneHotEncoder(handle_unknown='ignore')
        X_train_new = enc.fit_transform(X_train).toarray()
        X_test_new = enc.transform(X_test).toarray()
        mdl.fit(X_train_new, y_train)
        print("rf")
    else:
        pass
    
    #print('ani just upar')
    #print(np.array([1,2,3]))
    #print(reg.predict(np.array([[1,2,3]])))

    #prediction = reg.predict(X_test)

    #pkl_filename = document + ".pkl"

    return mdl, enc