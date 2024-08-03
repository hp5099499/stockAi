import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from stocknews import StockNews

# Set page title and favicon
# st.set_page_config(
#     page_title="Customized Stock Dashboard",
#     page_icon="📈",
#     layout="wide"
# )

# Custom CSS styles
st.markdown(
    """
    <style>
        .full-width {
            width: 100%;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .header-title {
            font-size: 36px;
            font-weight: bold;
        }
        .header-logo {
            font-size: 48px;
        }
        .section-header {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .sub-header {
            font-size: 18px;
            margin-top: 20px;
        }
        .styled-table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }
        .styled-table th, .styled-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .styled-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .news-container {
            margin-top: 10px;
        }
        .news-item {
            margin-bottom: 20px;
        }
        .news-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .news-details {
            font-size: 16px;
        }
        .positive-growth {
            color: green;
        }
        .negative-growth {
            color: red;
        }

        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                align-items: flex-start;
            }
            .section-header {
                font-size: 20px;
                margin-bottom: 5px;
            }
            .sub-header {
                font-size: 16px;
                margin-top: 10px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title and header
st.subheader("Stock Dashboard")
st.markdown("<hr>", unsafe_allow_html=True)

# # Define a function to be executed when the button is clicked
# def button_function():
#     st.write("Button clicked!")

# # Create a button with a label and a function
# if st.button('Click me'):
#     button_function()


# Sidebar inputs
ticker = st.sidebar.text_input("Enter Stock Symbol", "MSFT")
st.sidebar.markdown('Note. Use <a href="https://finance.yahoo.com" target="_blank">yfinance</a> for searching the stocks symbol.', unsafe_allow_html=True)
start_date = st.sidebar.date_input("Start Date", value=None)
end_date = st.sidebar.date_input("End Date")

# Fetching data using yfinance
data = yf.download(ticker, start=start_date, end=end_date)
st.markdown(ticker)

st.header(f"{data.Close.iloc[-1]:.2f}" )

p_d=data.Close.iloc[-1]-data.Open[1]
pd_p=(p_d/data.Open[1])*100
color = "green" if p_d >= 0 else "red"
st.markdown(f"<h1 style='color:{color};font-size: 15px;padding:0px'>{p_d:.2f} ({pd_p:.2f})%</h1>", unsafe_allow_html=True)

# Plotting price data using Plotly
fig = px.line(data, x=data.index, y=data['Adj Close'])
fig.update_traces(line=dict(color=color))

st.plotly_chart(fig)

# Creating tabs for different sections
performance_metrics, fundamental_data, news = st.tabs(["Performance Metrics","Fundamental Data","Top 10 News"])

# Pricing Data Section
with performance_metrics:
    st.markdown("<div class='section-header'>Performance Metrics</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='sub-header'>Price Movement</div>", unsafe_allow_html=True)

    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)

    # Calculating annual return, standard deviation, and risk-adjusted return
    annual_return = data2['% Change'].mean() * 252 * 100
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    risk_adj_return = annual_return / stdev if stdev != 0 else 0

    # Displaying formatted values with growth symbols
    col1,col2,col3=st.columns(3)
    with col1:
          growth_symbol = lambda x: "📈" if x > 0 else "📉" if x < 0 else ""
          st.header(f"{annual_return:.2f}% {growth_symbol(annual_return)}")
          st.write("Annual Return (%)")
    with col2:
          st.header(f"{stdev * 100:.2f}% {growth_symbol(stdev)}")
          st.write('Standard Deviation (%)')
    with col3:
       st.header(f"{risk_adj_return:.2f} {growth_symbol(risk_adj_return)}")
       st.write('Risk Adj. Return')

# Fundamental Data Section (using yfinance for some fundamental data)
with fundamental_data:

# Layout the section header
    st.markdown("<div class='section-header'>Fundamental Data</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    try:
        info = yf.Ticker(ticker).info
     
        # General Info
        st.markdown("<div class='sub-header'>General Info</div>", unsafe_allow_html=True)
        general_info = {
             "Company Name": [info.get('longName', 'N/A')],
             "Sector": [info.get('sector', 'N/A')],
             "Industry": [info.get('industry', 'N/A')],
             "Country": [info.get('country', 'N/A')]
         }
        general_info_df = pd.DataFrame(general_info)
        st.table(general_info_df)

         # Key Stats
        st.markdown("<div class='sub-header'>Key Stats</div>", unsafe_allow_html=True)
        key_stats = {
             "Market Cap": [f"{info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else 'N/A'],
             "Forward PE Ratio": [info.get('forwardPE', 'N/A')],
             "Dividend Yield": [f"{info.get('dividendYield', 0):.2%}" if info.get('dividendYield') else 'N/A']
         }
        key_stats_df = pd.DataFrame(key_stats)
        st.table(key_stats_df)
    

    except Exception as e:
        st.warning("Could not retrieve fundamental data.")
        st.write(f"Error: {e}")


# News Section
with news:
    st.markdown("<div class='section-header'>News</div>", unsafe_allow_html=True)
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()

    # Displaying top 10 news articles
    for i in range(min(10, len(df_news))):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='news-item'>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-title'>{df_news['title'][i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-details'><b>Published:</b> {df_news['published'][i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-details'>{df_news['summary'][i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-details'><b>Title Sentiment:</b> {df_news['sentiment_title'][i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-details'><b>News Sentiment:</b> {df_news['sentiment_summary'][i]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)