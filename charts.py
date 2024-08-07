import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# Title of the app
st.subheader('Stock Data Viewer with Various Charts')

# Time range mapping
time_range_map = {
    "1m": ("1mo", "1d"),
    "6m": ("6mo", "1wk"),
    "1y": ("1y", "1d"),
    "5y": ("5y", "1mo"),
    "all": ("max", "3mo")
}

# Option to choose between time range or fixed date range
range_option = st.sidebar.radio("Select Range Type", ["Fixed Date Range", "Time Range"])

# Input for stock ticker
ticker = st.sidebar.text_input('Enter Stock Ticker', 'AAPL')

if ticker:
    if range_option == "Time Range":
        # Selector for time range
        time_range = st.sidebar.selectbox("Select Time Range", list(time_range_map.keys()))

        # Get the period and interval from time_range_map
        period, interval = time_range_map[time_range]

        # Download the stock data
        stock_data = yf.download(ticker, period=period, interval=interval)

        st.write(f'Stock data for {ticker} with {time_range} range')

    elif range_option == "Fixed Date Range":
        # Calculate the date range
        end_date = datetime.now() - timedelta(days=1)  # Yesterday
        start_date = end_date - timedelta(days=7)  # One week ago

        # Convert dates to strings
        end_date_str = end_date.strftime('%Y-%m-%d')
        start_date_str = start_date.strftime('%Y-%m-%d')

        # Download the stock data
        stock_data = yf.download(ticker, start=start_date_str, end=end_date_str)

        st.write(f'Stock data for {ticker} from {start_date_str} to {end_date_str}')

    # Ensure stock_data is not empty before proceeding
    if not stock_data.empty:
        # Define the dates you want to remove
        dates_to_remove = [datetime(2024, 7, 27), datetime(2024, 7, 28)]  # Update these dates as needed

        # Convert the list of dates to strings in the format used by stock_data.index
        dates_to_remove_str = [date.strftime('%Y-%m-%d') for date in dates_to_remove]

        # Check if these dates are present in the stock data
        available_dates_to_remove = [date for date in dates_to_remove_str if date in stock_data.index.strftime('%Y-%m-%d')]

        # Filter out specific dates if they exist
        if available_dates_to_remove:
            stock_data = stock_data.loc[~stock_data.index.strftime('%Y-%m-%d').isin(available_dates_to_remove)]

        # Display the stock data
        # st.dataframe(stock_data)

        # Create a container with columns for buttons
        
        col1, col2, col3 ,col4= st.tabs(["LineChart","OHLC chart","Candles stick","Bar chart"])

        with col1:
                
                    if not stock_data.empty:
                        # Line plot of stock data for prediction (example implementation)
                        fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{ticker} Price Over Time')
                        st.plotly_chart(fig)
                    else:
                        st.write('No data available for sentiment prediction.')

        with col2:
                
                    if not stock_data.empty:
                        # OHLC chart of stock data (example implementation)
                        fig = go.Figure(data=[go.Ohlc(
                            x=stock_data.index,
                            open=stock_data['Open'],
                            high=stock_data['High'],
                            low=stock_data['Low'],
                            close=stock_data['Close']
                        )])
                        fig.update_layout(
                            title=f'OHLC Chart for {ticker}',
                            xaxis_title='Date',
                            yaxis_title='Price',
                            xaxis_rangeslider_visible=False
                        )
                        st.plotly_chart(fig)
                    else:
                        st.write('No data available for OHLC chart.')

        with col3:
                
                    if not stock_data.empty:
                        # Create the candlestick chart
                        fig = go.Figure(data=[go.Candlestick(
                            x=stock_data.index,
                            open=stock_data['Open'],
                            high=stock_data['High'],
                            low=stock_data['Low'],
                            close=stock_data['Close']
                        )])
            
                        # Calculate missing dates for range breaks
                        all_days = set(stock_data.index.date)
                        dates_to_remove_dates = set(date.date() for date in dates_to_remove)
                        missing_dates = sorted(dates_to_remove_dates - all_days)

                        # Convert missing dates to a list of Timestamp objects
                        missing_dates_timestamps = [pd.Timestamp(date) for date in missing_dates]
            
                        # Update the layout of the chart
                        fig.update_layout(
                            title=f'Candlestick Chart for {ticker}',
                            xaxis_title='Date',
                            yaxis_title='Price',
                            xaxis_rangeslider_visible=False
                        )
            
                        # Add range breaks to exclude missing dates
                        if missing_dates_timestamps:
                            fig.update_xaxes(rangebreaks=[dict(values=missing_dates_timestamps)])
            
                        # Display the candlestick chart
                        st.plotly_chart(fig)
                    else:
                        st.write('No data available for the selected date range.')
        
        with col4:
                    if not stock_data.empty:
                        # Bar chart of stock data (example implementation)
                        fig = px.bar(stock_data, x=stock_data.index, y='Volume', title=f'{ticker} Trading Volume Over Time')
                        st.plotly_chart(fig)
                    else:
                        st.write('No data available for bar chart.')
