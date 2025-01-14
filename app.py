import streamlit as st

# Import pages
from twitter_sentiment_analysis import run_twitter_sentiment_analysis
from stock_sentiment_analysis import run_stock_sentiment_analysis
from stock_trend_prediction import run_stock_trend_prediction

# Define the pages in the app
pages = {
    "Twitter Sentiment Analysis": run_twitter_sentiment_analysis,
    "Stock Sentiment Analysis": run_stock_sentiment_analysis,
    "Stock Trend Prediction": run_stock_trend_prediction,
}

# Streamlit navigation
st.title("Sentiment Analysis and Stock Prediction App")
page_selection = st.sidebar.selectbox("Select a page:", options=list(pages.keys()))

# Run the selected page
pages[page_selection]()
