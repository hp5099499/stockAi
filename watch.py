import streamlit as st
import yfinance as yf
import json
import os

# File to store watchlists
WATCHLIST_FILE = 'watchlists.json'

def load_watchlists():
    """Load watchlists from the JSON file."""
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_watchlist(name, tickers):
    """Save the watchlist to the JSON file."""
    watchlists = load_watchlists()
    watchlists[name] = tickers
    with open(WATCHLIST_FILE, 'w') as file:
        json.dump(watchlists, file)

def delete_watchlist(name):
    """Delete a watchlist from the JSON file."""
    watchlists = load_watchlists()
    if name in watchlists:
        del watchlists[name]
        with open(WATCHLIST_FILE, 'w') as file:
            json.dump(watchlists, file)

def get_stock_data(ticker):
    """Fetch stock data for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        # Fetching the most recent closing price
        history = stock.history(period='1d')
        latest_close = history['Close'].iloc[-1] if not history.empty else 'N/A'
        latest_close = f"{latest_close:.2f}" if isinstance(latest_close, float) else latest_close
        trailing_pe = stock_info.get('trailingPE', 'N/A')
        trailing_pe = f"{trailing_pe:.2f}" if isinstance(trailing_pe, float) else trailing_pe
        return {
            'Name': stock_info.get('shortName', 'N/A'),
            'Price': latest_close,
            'Market Cap': stock_info.get('marketCap', 'N/A'),
            'P/E Ratio': trailing_pe,
            '52 Week High': stock_info.get('fiftyTwoWeekHigh', 'N/A'),
            '52 Week Low': stock_info.get('fiftyTwoWeekLow', 'N/A'),
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

st.title('🔖 Stock Watchlist')

# Section to add, view, and delete watchlists
st.sidebar.header('Manage Watchlists')

watchlists = load_watchlists()

def display_stock_data(stock_data):
    colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffb3e6"]
    cols = st.columns(3)
    col_data = list(stock_data.items())
    for i, (key, value) in enumerate(col_data):
        color = colors[i % len(colors)]
        with cols[i % 3]:
            st.markdown(f"<div style='color: {color}; font-weight: bold;'>{key}:</div> <div style='color: {color};'>{value}</div>", unsafe_allow_html=True)

if watchlists:
    selected_watchlist = st.sidebar.selectbox("Select a watchlist to view:", options=list(watchlists.keys()) + ["Create New"])
    
    if selected_watchlist != "Create New":
        tickers = watchlists[selected_watchlist]
        with st.container():
            st.subheader(f"Watchlist Name: {selected_watchlist}")
            for ticker in tickers:
                with st.expander(f"Data for {ticker}"):
                    stock_data = get_stock_data(ticker)
                    if stock_data:
                        display_stock_data(stock_data)
                    st.write("---")
        if st.sidebar.button(f"Delete {selected_watchlist}"):
            delete_watchlist(selected_watchlist)
            st.success(f"Watchlist '{selected_watchlist}' deleted successfully!")
            st.rerun()
else:
    st.write("No watchlists found.")

# Section to create or update watchlists
st.sidebar.header('Create or Update Watchlist')

with st.sidebar.container():
    watchlist_name = st.text_input("Enter a name for your watchlist:")
    tickers_input = st.text_input("Enter stock tickers (comma-separated):")

    if st.button("Save Watchlist"):
        if watchlist_name and tickers_input:
            tickers_list = [ticker.strip().upper() for ticker in tickers_input.split(',')]
            save_watchlist(watchlist_name, tickers_list)
            st.success(f"Watchlist '{watchlist_name}' saved successfully!")
            st.rerun()
        else:
            st.error("Please enter both a watchlist name and tickers.")

st.sidebar.write("Enter a name and tickers to create or update a watchlist.")

# Add custom CSS for animation
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .stContainer > div {
        animation: fadeIn 1s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)