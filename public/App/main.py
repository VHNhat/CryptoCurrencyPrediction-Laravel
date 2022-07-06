from operator import index
import sys
import pandas as pd
import datetime as dt
import numpy as np
import investpy
import json
from dateutil.relativedelta import relativedelta

from keras.models import load_model

from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.preprocessing import MinMaxScaler

scala_x = MinMaxScaler(feature_range=(0,1))
scala_y = MinMaxScaler(feature_range=(0,1))
ma_1 = 7
ma_2 = 14
ma_3 = 21
cols_x = ['H-L', 'O-C', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'SD_{ma_1}', f'SD_{ma_3}']
cols_y = ['Close']

def PreProcessing(df,pre_day, test_size):
    df.pop('Currency')
    df.pop('Volume')
    df['Open'] = df['Open'] / 1000
    df['High'] = df['High'] / 1000
    df['Low'] = df['Low'] / 1000
    df['Close'] = df['Close'] / 1000

    # Process data
    df['H-L'] = df['High'] - df['Low']
    df['O-C'] = df['Open'] - df['Close']
    
    df[f'SMA_{ma_1}'] = df['Close'].rolling(window=ma_1).mean()
    df[f'SMA_{ma_2}'] = df['Close'].rolling(window=ma_2).mean()
    df[f'SMA_{ma_3}'] = df['Close'].rolling(window=ma_3).mean()

    df[f'SD_{ma_1}'] = df['Close'].rolling(window=ma_1).std()
    df[f'SD_{ma_3}'] = df['Close'].rolling(window=ma_3).std()
    df.dropna(inplace=True)

    
    scaled_data_x = scala_x.fit_transform(df[cols_x].values.reshape(-1, len(cols_x)))
    scaled_data_y = scala_y.fit_transform(df[cols_y].values.reshape(-1, len(cols_y)))

    x_total = []
    y_total = []

    for i in range(pre_day, len(df)):
        x_total.append(scaled_data_x[i-pre_day:i])
        y_total.append(scaled_data_y[i])

    x_train = np.array(x_total[:len(x_total)-test_size])
    x_test = np.array(x_total[len(x_total)-test_size:])
    y_train = np.array(y_total[:len(y_total)-test_size])
    y_test = np.array(y_total[len(y_total)-test_size:])

    return df, x_train, x_test, y_train, y_test

def CrawlData(crypto):
    
    start = (dt.datetime.today()-relativedelta(years=2)).strftime("%d/%m/%Y")
    end = dt.datetime.today().strftime("%d/%m/%Y")
    # Crawl data
    return investpy.get_crypto_historical_data(crypto = crypto, from_date=start, to_date=end)

if __name__ == '__main__':
    crypto = sys.argv[1]
    df = CrawlData(crypto)

    pre_day = 30
    test_size = (int)(len(df) * 0.2)

    df, x_train, x_test, y_train, y_test = PreProcessing(df, pre_day, test_size)
    
    model = load_model(f"C:/xampp/htdocs/nckh/public/App/{crypto}_laravel.h5")
    # Testing
    predict_price = model.predict(x_test,verbose=0)
    predict_price = scala_y.inverse_transform(predict_price)

    # Ploting the stat
    real_price = df[len(df)-test_size:]['Close'].values.reshape(-1,1)
    real_price = np.array(real_price)
    real_price = real_price.reshape(real_price.shape[0], 1)

    df_pred = pd.DataFrame()
    df_pred['Date'] = df.index[len(df)-test_size:].strftime("%Y-%m-%d")
    df_pred['Actual'] = real_price
    df_pred['Predict'] = predict_price

    # Make Prediction
    next_pred = pd.DataFrame(columns=['Date', 'Actual', 'Predict'])
    Date = []
    Actual = []
    Predict = []
    for i in range(5):
        Date.append((dt.datetime.today() + dt.timedelta(days=(i+1))).strftime("%Y-%m-%d"))
        x_predict = df[(len(df)-pre_day)+(i+1):][cols_x].values.reshape(-1, len(cols_x))
        x_predict = scala_x.transform(x_predict)
        x_predict = np.array(x_predict)
        x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))

        prediction = model.predict(x_predict,verbose=0)
        prediction = scala_y.inverse_transform(prediction)
        Actual.append(-1)
        Predict.append(prediction[0][0])

    next_pred['Date'] = Date
    next_pred['Actual'] = Actual
    next_pred['Predict'] = Predict
    next_pred.set_index('Date')
    df_pred = pd.concat([df_pred,next_pred])
    df_pred.set_index('Date')
    df_pred.to_csv(f'C:/xampp/htdocs/nckh/public/App/{crypto}_laravel.csv', index=False)
    
    head = "{" + f'"{crypto}":['
    tail = "]}"
    result = head+(df_pred.to_json(orient='records')[1:-1].replace('},{', '},\n{'))+tail
    with open(f'{crypto}.json', 'w') as f:
        f.write(result)
    json_data = json.dumps(result)
    print(json_data)