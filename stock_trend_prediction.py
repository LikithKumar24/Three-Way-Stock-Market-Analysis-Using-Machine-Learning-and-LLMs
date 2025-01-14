import yfinance as yf
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import load_model
import streamlit as st

def run_stock_trend_prediction():
    start = '2015-01-01'
    end='2024-12-31'

    st.title('Stock Trend Prediction')

    user_input = st.text_input('Enter the Stock Ticker', 'AAPL')

    df = yf.download(user_input, start=start, end=end)

    if df.empty:
        st.error("No data found for this ticker.")
        return

    st.subheader('Data from 2015-2024')
    st.write(df.describe())

    # Plotting Closing Price vs Time Chart
    fig=plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    plt.title('Closing Price vs Time Chart')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    st.pyplot(fig)

    # Plotting Moving Averages (100 MA)
    ma100=df.Close.rolling(100).mean()
    
    fig=plt.figure(figsize=(12,6))
    plt.plot(ma100, label='100 MA')
    plt.plot(df.Close, label='Closing Price')
    
    plt.title('Closing Price vs Time Chart with Moving Average [100 MA]')
    plt.xlabel('Date')
    plt.ylabel('Price')
    
    plt.legend()
    
    st.pyplot(fig)

   # Plotting Moving Averages (200 MA)
    ma200=df.Close.rolling(200).mean()
   
    fig=plt.figure(figsize=(12,6))
    plt.plot(ma100, label='100 MA')
    plt.plot(ma200, label='200 MA')
    plt.plot(df.Close, label='Closing Price')
   
    plt.title('Closing Price vs Time Chart with Moving Average [200 MA]')
    plt.xlabel('Date')
    plt.ylabel('Price')
   
    plt.legend()
   
    st.pyplot(fig)

    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing=pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(0,1))

    data_training_array=scaler.fit_transform(data_training)

    model = load_model('keras_model_3.h5')

    past_100_days=data_training.tail(100)

    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)

    input_data=scaler.fit_transform(final_df)

    x_test =[]
    y_test=[]

    for i in range(100, input_data.shape[0]):
       x_test.append(input_data[i-100:i])
       y_test.append(input_data[i,0])

    x_test,y_test=np.array(x_test),np.array(y_test)

    y_predicted=model.predict(x_test)

    scaler_scale_factor = scaler.scale_

    scale_factor = 1 / scaler_scale_factor 
    y_predicted = y_predicted * scale_factor 
    y_test = y_test * scale_factor 

   # Plotting Predictions vs Original Prices 
    fig2=plt.figure(figsize=(12,6))
    plt.plot(y_test,'b',label='Original Price')
    plt.plot(y_predicted,'r',label='Predicted Price')
   
    plt.title('Predictions vs Original Prices')
    plt.xlabel('Time')
    plt.ylabel('Price')
   
    plt.legend()
   
    st.pyplot(fig2)
