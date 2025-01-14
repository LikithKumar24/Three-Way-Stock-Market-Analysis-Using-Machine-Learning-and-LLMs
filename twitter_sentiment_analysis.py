import streamlit as st
import tweepy
from transformers import pipeline
import time

# Replace with your Bearer Token
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIZsyAEAAAAAKtOKisYS1MizUDZyEhPE17TY%2FtI%3DMoaosqZG1Dn30myt5UEkhLIe1xt27pgNlm0vF0KQo20T0JqJaN'

# Set up tweepy client using Bearer Token authentication
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline(task="text-classification", model="ProsusAI/finbert")

def fetch_tweets(search_term, tweet_amount=10):
    try:
        # Fetch tweets using the Tweepy Client with Bearer Token
        tweets = client.search_recent_tweets(query=search_term, max_results=tweet_amount)
        return tweets.data if tweets.data else []
    except tweepy.TweepyException as e:
        st.error(f"An error occurred: {e}")
        return []

def analyze_sentiment(tweets):
    results = []
    for tweet in tweets:
        sentiment = sentiment_pipeline(tweet.text)[0]
        results.append({
            'text': tweet.text,
            'sentiment': sentiment['label'],
            'score': sentiment['score']
        })
        time.sleep(1)  # Added a delay to avoid hitting rate limits
    return results

def run_twitter_sentiment_analysis():
    st.title("Twitter Sentiment Analysis")
    st.write("Enter a search term to analyze recent tweets.")

    search_term_input = st.text_input("Search Term (e.g., stocks):")
    tweet_amount_input = st.number_input("Number of Tweets to Fetch:", min_value=1, max_value=100, value=10)

    if st.button("Analyze"):
        if search_term_input:
            with st.spinner("Fetching and analyzing tweets..."):
                tweets = fetch_tweets(search_term_input, tweet_amount_input)
                if tweets:
                    analyzed_results = analyze_sentiment(tweets)
                    
                    # Display results
                    st.subheader("Sentiment Analysis Results")
                    for result in analyzed_results:
                        st.markdown(f"**Tweet:** {result['text']}")
                        st.write(f"**Sentiment:** {result['sentiment']}, Score: {result['score']:.2f}")
                        st.write("---")
                else:
                    st.write("No tweets found for the given search term.")
        else:
            st.error("Please enter a search term.")
