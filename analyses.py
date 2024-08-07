import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator, SMAIndicator
from ta.momentum import RSIIndicator
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import time

st.subheader('Stock Price Predictions')

def main():
    option = st.sidebar.selectbox('Make a choice', ['Visualize', 'Recent Data', 'Predict'])
    if option == 'Visualize':
        tech_indicators()
    elif option == 'Recent Data':
        update_data_and_plot()
        # st.markdown("[more...](https://predictre.streamlit.app)")

    elif option == 'Predict':
        predict()
    

# @st.cache_resource
def download_data(op, start_date, end_date):
    df = yf.download(op, start=start_date, end=end_date, progress=False)
    return df

option = st.sidebar.text_input('Enter a Stock Symbol', value='SPY')
option = option.upper()
today = datetime.today().date()
duration = st.sidebar.number_input('Enter the duration', value=3000)
before = today - timedelta(days=duration)
start_date = st.sidebar.date_input('Start Date', value=before)
end_date = st.sidebar.date_input('End date', today)
if st.sidebar.button('Send'):
    if start_date < end_date:
        st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
        data = download_data(option, start_date, end_date)
    else:
        st.sidebar.error('Error: End date must fall after start date')

data = download_data(option, start_date, end_date)
scaler = StandardScaler()

# Compute the price difference and percentage change
p_d = data.Close.iloc[-1] - data.Open.iloc[1]
pd_p = (p_d / data.Open.iloc[1]) * 100

def tech_indicators():
    st.header('Technical Indicators')
    option = st.radio('Choose a Technical Indicator to Visualize', ['Close', 'BB', 'MACD', 'RSI', 'SMA', 'EMA'])

    # Bollinger bands
    bb_indicator = BollingerBands(data.Close)
    bb = data.copy()
    bb['bb_h'] = bb_indicator.bollinger_hband()
    bb['bb_l'] = bb_indicator.bollinger_lband()
    # Creating a new dataframe
    bb = bb[['Close', 'bb_h', 'bb_l']]
    # MACD
    macd = MACD(data.Close).macd()
    # RSI
    rsi = RSIIndicator(data.Close).rsi()
    # SMA
    sma = SMAIndicator(data.Close, window=14).sma_indicator()
    # EMA
    ema = EMAIndicator(data.Close).ema_indicator()

    if option == 'Close':
        st.write('Close Price')
        st.line_chart(data['Close'])
    elif option == 'BB':
        st.write('BollingerBands')
        st.line_chart(bb)
    elif option == 'MACD':
        st.write('Moving Average Convergence Divergence')
        st.line_chart(macd)
    elif option == 'RSI':
        st.write('Relative Strength Indicator')
        st.line_chart(rsi)
    elif option == 'SMA':
        st.write('Simple Moving Average')
        st.line_chart(sma)
    else:
        st.write('Exponential Moving Average')
        st.line_chart(ema)

def fetch_stock_data(ticker, period="1d", interval="1m"):
    return yf.Ticker(ticker).history(period=period, interval=interval)

def update_data_and_plot():
    st.title("Real-Time Stock Data")
    ticker=option
    time_range = st.selectbox("Select the time range:", ["1d"])

    # Time range mapping
    time_range_map = {
        "1d": ("1d", "5m"),
    }

    if ticker and time_range:
        period, interval = time_range_map.get(time_range, ("1d", "5m"))
        data = fetch_stock_data(ticker, period, interval)

        # Initialize session state
        if "historical_data" not in st.session_state:
            st.session_state.historical_data = pd.DataFrame()
        if "last_data_point" not in st.session_state:
            st.session_state.last_data_point = None
        if "same_data_time" not in st.session_state:
            st.session_state.same_data_time = None
        if "last_update_time" not in st.session_state:
            st.session_state.last_update_time = datetime.now()
        if "auto_update" not in st.session_state:
            st.session_state.auto_update = False
        if "update_stopped" not in st.session_state:
            st.session_state.update_stopped = False

        chart_placeholder = st.empty()
        table_placeholder = st.empty()

        def update_data_and_plot():
            new_data = fetch_stock_data(ticker, period, interval)
            if not new_data.empty:
                current_data_point = new_data.iloc[-1]['Close']
                if st.session_state.last_data_point == current_data_point:
                    if st.session_state.same_data_time is None:
                        st.session_state.same_data_time = datetime.now()
                    elif datetime.now() - st.session_state.same_data_time > timedelta(minutes=5):
                        st.write("Data unchanged for 5 minutes. Stopping updates.")
                        st.session_state.auto_update = False
                        st.session_state.update_stopped = True
                        return
                else:
                    st.session_state.same_data_time = None

                st.session_state.last_data_point = current_data_point
                st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data]).drop_duplicates()

                fig = go.Figure(data=[go.Candlestick(
                    x=st.session_state.historical_data.index,
                    open=st.session_state.historical_data['Open'],
                    high=st.session_state.historical_data['High'],
                    low=st.session_state.historical_data['Low'],
                    close=st.session_state.historical_data['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red'
                )])
                fig.update_layout(title=f"{ticker} - Real-Time Data", xaxis_title="Time", yaxis_title="Price")
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                st.session_state.last_update_time = datetime.now()
                st.session_state.update_stopped = False
                table_placeholder.dataframe(st.session_state.historical_data)

        if st.button("Start Automatic Updates"):
            st.session_state.auto_update = True
            st.session_state.update_stopped = False

        if st.button("Stop Automatic Updates"):
            st.session_state.auto_update = False
            st.session_state.update_stopped = True

        if st.session_state.auto_update:
            update_data_and_plot()
            time.sleep(15)
            st.rerun()

        if st.session_state.update_stopped:
            st.write("Updates have stopped. Showing the last updated data.")
            fig = go.Figure(data=[go.Candlestick(
                x=st.session_state.historical_data.index,
                open=st.session_state.historical_data['Open'],
                high=st.session_state.historical_data['High'],
                low=st.session_state.historical_data['Low'],
                close=st.session_state.historical_data['Close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )])
            fig.update_layout(title=f"{ticker} - Last Updated Data", xaxis_title="Time", yaxis_title="Price")
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            table_placeholder.dataframe(st.session_state.historical_data)

def predict():
    num = st.number_input('How many days forecast?', value=5)
    num = int(num)
    if st.button('Predict'):
        model_engine(num)

def model_engine(num):
    # getting only the closing price
    df = data[['Close']]
    # shifting the closing price based on number of days forecast
    df['preds'] = data.Close.shift(-num)
    # scaling the data
    x = df.drop(['preds'], axis=1).values
    x = scaler.fit_transform(x)
    # storing the last num_days data
    x_forecast = x[-num:]
    # selecting the required values for training
    x = x[:-num]
    # getting the preds column
    y = df.preds.values
    # selecting the required values for training
    y = y[:-num]

    # splitting the data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=7)
    # training the model
    model = LinearRegression()
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    col1, col2 = st.columns(2)
    with col1:
        st.info(f'Accuracy score: {r2_score(y_test, preds) * 100:.2f}%')
    with col2:
        st.info(f'MAE: {mean_absolute_error(y_test, preds):.2f}')
    # predicting stock price based on the number of days
    forecast_pred = model.predict(x_forecast)
    forecast_dates = pd.date_range(start=data.index[-1], periods=num + 1).tolist()[1:]
    forecast_df = pd.DataFrame(forecast_pred, index=forecast_dates, columns=['Forecast'])

    # Combine historical data with forecast data
    combined_df = pd.concat([data[['Close']], forecast_df])

    st.line_chart(combined_df)

if __name__ == '__main__':
    main()
