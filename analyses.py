import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import math

st.title("Stock Price Prediction Using LSTM")

# Step 1: Fetch data from Yahoo Finance
def fetch_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df1 = df['Close']  # Use the 'Close' price for predictions
    return df1

# Sidebar for user input
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2019-01-01"))  # 3 years before end date
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2022-01-01"))

# Fetch data based on user input
df1 = fetch_data(ticker, start_date, end_date)

if df1.empty:
    st.write("No data found for the given ticker symbol and date range.")
else:
    st.write(f"### Stock Closing Prices for {ticker}")
    st.line_chart(df1)

    # Step 2: Preprocess the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    df1_scaled = scaler.fit_transform(np.array(df1).reshape(-1, 1))

    # Splitting dataset into train and test split
    training_size = int(len(df1_scaled) * 0.65)
    test_size = len(df1_scaled) - training_size
    train_data, test_data = df1_scaled[0:training_size, :], df1_scaled[training_size:len(df1_scaled), :]

    # Convert an array of values into a dataset matrix
    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]   
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    # Reshape into X=t, t+1, t+2, t+3 and Y=t+4
    time_step = 100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    # Reshape input to be [samples, time steps, features] which is required for LSTM
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Create the Stacked LSTM model
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(time_step, 1)))
    model.add(LSTM(80, return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    model.summary()

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=64, verbose=1)

    # Prediction
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Transform back to original form
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)
    y_train_inv = scaler.inverse_transform(y_train.reshape(-1, 1))
    y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Calculate performance metrics
    train_rmse = math.sqrt(mean_squared_error(y_train_inv, train_predict))
    test_rmse = math.sqrt(mean_squared_error(y_test_inv, test_predict))
    train_mae = mean_absolute_error(y_train_inv, train_predict)
    test_mae = mean_absolute_error(y_test_inv, test_predict)
    train_r2 = r2_score(y_train_inv, train_predict)
    test_r2 = r2_score(y_test_inv, test_predict)
    # st.markdown("Performance Metrics")

    # col1, col2 ,col3= st.columns(3)
    
    # # Add metrics to the first column
    # with col1:
    #     st.write(f"**Train RMSE:** {train_rmse}")
    #     st.write(f"**Test RMSE:** {test_rmse}")
    
    # # Add metrics to the second column
    # with col2:
    #     st.write(f"**Train MAE:** {train_mae}")
    #     st.write(f"**Test MAE:** {test_mae}")
       
    # with col3:
    #      st.write(f"**Train R2:** {train_r2}")
    #      st.write(f"**Test R2:** {test_r2}")
    # Plotting
    # Shift train predictions for plotting
    look_back = time_step
    trainPredictPlot = np.empty_like(df1_scaled)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict

    # Shift test predictions for plotting
    testPredictPlot = np.empty_like(df1_scaled)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(df1_scaled) - 1, :] = test_predict

    # Plot baseline and predictions
    plt.figure(figsize=(12, 6))
    plt.plot(scaler.inverse_transform(df1_scaled), label="Original Data")
    plt.plot(trainPredictPlot, label="Train Predictions")
    plt.plot(testPredictPlot, label="Test Predictions")
    plt.legend()
    # st.pyplot(plt)

    # Forecasting for next 365 days
    x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
    temp_input = list(x_input[0])

    lst_output = []
    n_steps = time_step
    i = 0
    while i < 365:
        if len(temp_input) > time_step:
            x_input = np.array(temp_input[1:])
            x_input = x_input.reshape(1, -1)
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            temp_input = temp_input[1:]
            lst_output.extend(yhat.tolist())
            i += 1
        else:
            x_input = x_input.reshape((1, n_steps, 1))
            yhat = model.predict(x_input, verbose=0)
            temp_input.extend(yhat[0].tolist())
            lst_output.extend(yhat.tolist())
            i += 1

    st.write("### Next 1 year Prediction")

    # Plot the forecasted data
    day_new = np.arange(1, len(df1_scaled) + 1)
    day_pred = np.arange(len(df1_scaled) + 1, len(df1_scaled) + 366)

    plt.figure(figsize=(12, 6))
    plt.plot(day_new, scaler.inverse_transform(df1_scaled), label="Last 100 Days")
    plt.plot(day_pred, scaler.inverse_transform(lst_output), label="Next 1 year Days")
    plt.legend()
    # st.pyplot(plt)

    df3 = df1_scaled.tolist()
    df3.extend(lst_output)
    df3 = scaler.inverse_transform(df3).tolist()

    plt.figure(figsize=(12, 6))
    plt.plot(df3, label="Extended Data")
    plt.legend()
    st.pyplot(plt)
