import streamlit as st
import pandas as pd

# Define CSS classes
css = """
<style>
*{
box-sizing:border-box;
}
.primary {
    color: white;
    background-color: blue;
    padding: 40px;
    border-radius: 5px;
    height:100px;
    text-align:center;
    margin:10px;

}

.secondary {
    # font-size: 20px;
    font-weight: bold;
}

.warning {
    background-color: none;
    padding:20px;
    color: white;

}
.cols{
  border:5px solid blue;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
  width: 30%;
  height:100px;
  text-align:center;
  padding :10px;
  margin:0px 0px 0px 3px;
  border-radius:10px;
  float:left;
}

.cols:hover {
  box-shadow:  0px 8px 16px 0 brown;
}

.container {
  paddiing :2px 16px;
  
   }
   table{
   padding:10px;
   td{
   border:2px solid blue
   width:100%;
   height:30px;
   padding:10px;

   }
   }
</style>
"""

# Inject CSS into the Streamlit app
st.markdown(css, unsafe_allow_html=True)

# Use multiple CSS classes in an HTML element
html_content = """
<h1  class="primary secondary">
    Dashboard
</h1>
<div class="warning secondary">
<h4>Indices</h4>
   <div class="cols">NIFTY 50  <div>24,834</div> <div>+428.75(1.76)</div></div>
   <div class="cols">NIFTY BANK<div>51,295</div> <div>+407.20(0.80)%</div></div>
   <div class="cols">BSE SENSEX<div>81,332</div> <div>+1292.92(1.62)%</div></div>
</div>
"""

html_content1 ="""
</h1>
<div >
<h4> Top gainers</h4>
  <table>
  <th>
  <td>fx</td>
  <td></td>
  <td></td>
  
  </th>
  <tr>
   <td></td>
   <td></td>
  <td></td>
  <td></td>
  </tr>
</div>
"""

html_content2 ="""
</h1>
<div >
<h4> Top gainers</h4>
  <table>
  <th>
  <td></td>
  <td></td>
  <td></td>
  
  </th>
  <tr>
   <td></td>
   <td></td>
  <td></td>
  <td></td>
  </tr>
</div>
"""


# Render the HTML content in the Streamlit app
st.markdown(html_content, unsafe_allow_html=True)
# st.markdown(html_content1,unsafe_allow_html=True)
# st.markdown(html_content2,unsafe_allow_html=True)


import yfinance as yf
import pandas as pd
import streamlit as st

# Define a list of tickers for NSE and BSE
nse_tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS']  # Add more tickers as needed
bse_tickers = ['RELIANCE.BO', 'TCS.BO', 'INFY.BO', 'HDFCBANK.BO', 'HINDUNILVR.BO']  # Add more tickers as needed

# Combine both lists
all_tickers = nse_tickers + bse_tickers

# Function to get top gainers
def get_top_gainers(tickers):
    frames = []

    for ticker in tickers:
        try:
            # Fetch historical data
            stock = yf.Ticker(ticker)
            hist = stock.history(period='1d')
            hist['Ticker'] = ticker
            frames.append(hist)
        except Exception as e:
            print(f"Could not fetch data for {ticker}: {e}")

    if frames:
        # Concatenate all DataFrames
        gainers_df = pd.concat(frames)

        # Calculate the percentage change
        gainers_df['Percent Change'] = ((gainers_df['Close'] - gainers_df['Open']) / gainers_df['Open']) * 100

        # Sort by percentage change
        top_gainers = gainers_df.sort_values(by='Percent Change', ascending=False).head(10)

        return top_gainers
    else:
        return pd.DataFrame()

# Get the top gainers
top_gainers = get_top_gainers(all_tickers)

# Apply custom CSS
st.markdown("""
    <style>
        .title {
            font-size: 2em;
            color: #333;
            text-align: center;
            margin-bottom: 20px;
        }
        .table {
            margin-left: auto;
            margin-right: auto;
            width: 90%;
        }
        .table td, .table th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .table th {
            background-color: #000000;
            text-align: center;
        }
        .gainers-table {
            background-color: green;
        }
        .losers-table {
            background-color: red;
        }
        .alert {
            padding: 20px;
            background-color: #f44336;
            color: white;
            margin-bottom: 15px;
        }
        .notification-icon {
            color: green;
            font-size: 1.5em;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the top gainers in Streamlit
st.markdown("<div class='title'>Top Gainers for NSE and BSE</div>", unsafe_allow_html=True)
if not top_gainers.empty:
    top_gainers = top_gainers.set_index('Ticker')
    # st.markdown("<div clrass='notification-icon'>&#x1F4C8;</div>Top 10 Gainers", unsafe_allow_html=True)
    st.markdown(top_gainers[['Open', 'Close', 'Percent Change']].to_html(classes='table gainers-table'), unsafe_allow_html=True)
else:
    st.markdown("<div class='alert'>No data available.</div>", unsafe_allow_html=True)

# Display the top losers in Streamlit
st.markdown("<div class='title'>Top Losers for NSE and BSE</div>", unsafe_allow_html=True)
if not top_gainers.empty:
    top_losers = top_gainers.sort_values(by='Percent Change', ascending=True).head(10)
    # st.markdown("<div class='notification-icon'>&#x1F4C9;</div>Top 10 Losers", unsafe_allow_html=True)
    st.markdown(top_losers[['Open', 'Close', 'Percent Change']].to_html(classes='table losers-table'), unsafe_allow_html=True)
else:
    st.markdown("<div class='alert'>No data available.</div>", unsafe_allow_html=True)


# Add a disclaimer section
st.markdown("""
## Disclaimer

The content provided in this application is for informational purposes only. All rights to the content, including but not limited to text, images, and data, are owned by their respective copyright holders.

### Copyright Notice
All content and materials available on this site are protected by copyright law. Unauthorized use and/or duplication of this material without express and written permission from the author and/or owner is strictly prohibited.

### Fair Use
This application may contain copyrighted material the use of which has not always been specifically authorized by the copyright owner. We are making such material available in our efforts to advance understanding of issues related to the content provided. We believe this constitutes a 'fair use' of any such copyrighted material as provided for in section 107 of the US Copyright Law.

### External Links
This application may contain links to external websites that are not provided or maintained by or in any way affiliated with us. Please note that we do not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites.

### Limitation of Liability
The use of this application is at your own risk. In no event shall we be liable for any damages arising out of or in connection with the use or performance of this application or the information available from this application.

For more information, please contact us at  📧 
            himanshuchnm2021@gmail.com, surajitghosh368@gmail.com, mohitsscs1980@gmail.com
""")
