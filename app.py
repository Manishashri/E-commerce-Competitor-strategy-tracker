
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from openai import AzureOpenAI
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from transformers import pipeline

API_KEY = "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"  # Groq API Key
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"  # Slack webhook url

def truncate_text(text, max_length=512):
    return text[:max_length]

def load_competitor_data():
    data = pd.read_csv("competitor_data.csv")
    print(data.head())
    return data

def load_reviews_data():
    reviews = pd.read_csv("reviews.csv")
    return reviews

def analyze_sentiment(reviews):
    sentiment_pipeline = pipeline("sentiment-analysis")
    return sentiment_pipeline(reviews)

def train_predictive_model(data):
    data["Discount"] = data["Discount"].str.replace("%", "").astype(float)
    data["Price"] = data["Price"].astype(int)

    data["Predicted_Discount"] = data["Discount"] + (data["Price"] * 0.05).round(2)

    X = data[["Price", "Discount"]]
    y = data["Predicted_Discount"]
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, train_size=0.8
    )

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model

import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
import streamlit as st
import plotly.express as px

# Forecast future discounts using ARIMA
def forecast_discounts_arima(data, future_days=5):
    """
    Forecast future discounts using ARIMA.
    :param data: DataFrame containing historical discount data (with a datetime index).
    :param future_days: Number of days to forecast.
    :return: DataFrame with historical and forecasted discounts.
    """
    try:
        # Ensure data is sorted by index
        data = data.sort_index()

        # Validate and clean the Discount column
        data["Discount"] = pd.to_numeric(data["Discount"], errors="coerce")
        data = data.dropna(subset=["Discount"])

        # Ensure the index is a datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            try:
                data.index = pd.to_datetime(data.index)
            except Exception as e:
                raise ValueError("Index must be datetime or convertible to datetime.") from e

        # Fit the ARIMA model
        discount_series = data["Discount"]
        model = ARIMA(discount_series, order=(5, 1, 0))  # Adjust parameters as needed
        model_fit = model.fit()

        # Forecast future values
        forecast = model_fit.forecast(steps=future_days)
        future_dates = pd.date_range(
            start=discount_series.index[-1] + pd.Timedelta(days=1), periods=future_days
        )
        forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Discount": forecast})

        # Adding the price column from the latest historical price (or interpolate if needed)
        forecast_df["Price"] = data["Price"].iloc[-1]  # Use the last known price

        # Ensure that forecasted Discount is also filled
        forecast_df["Discount"] = data["Discount"].iloc[-1]  # Use the last known discount

        forecast_df.set_index("Date", inplace=True)

        return pd.concat([data, forecast_df], axis=0)

    except Exception as e:
        st.error(f"ARIMA model failed: {e}")
        return data

# Send data to Slack
def send_to_slack(data):
    payload = {"text": data}
    response = requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    return response


# Generate strategic recommendations
def generate_strategy_recommendation(product_name, competitor_data, sentiment):
    """
    Generate strategic recommendations using an LLM.
    """
    date = datetime.now()

    prompt = f"""
    You are a highly skilled business strategist specializing in e-commerce. Based on the following details, suggest strategies:

    1. **Product Name**: {product_name}
    2. **Competitor Data** (including current prices, discounts, and predicted discounts): {competitor_data}
    3. **Sentiment Analysis**: {sentiment}
    4. **Today's Date**: {str(date)}

    ### Task:
    - Analyze the competitor data and identify key pricing trends.
    - Leverage sentiment analysis insights to highlight areas where customer satisfaction can be improved.
    - Use the discount predictions to suggest how pricing strategies can be optimized over the next 5 days.
    - Recommend promotional campaigns or marketing strategies that align with customer sentiments and competitive trends.
    - Ensure the strategies are actionable, realistic, and geared toward increasing customer satisfaction, driving sales, and strengthening brand loyalty.

    Provide your recommendations in a structured format:
    1. **Pricing Strategy**
    2. **Promotional Campaign Ideas**
    3. **Customer Satisfaction Recommendations**
    """
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-8b-8192",
        "temperature": 0,
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(data),
        headers=headers,
    )
    res = res.json()
    response = res["choices"][0]["message"]["content"]
    return response


# Streamlit page configuration
st.set_page_config(page_title="E-Commerce Competitor Strategy Dashboard", layout="wide")

st.title("E-Commerce Competitor Strategy Dashboard")
st.sidebar.header("Select a Product")

# Products based on the table
products = [
    "Wireless Earbuds",
    "Fitness Tracker",
    "Smartwatch"
]
selected_product = st.sidebar.selectbox("Choose a product to analyze:", products)

# Load mock competitor data
@st.cache_data
def load_competitor_data():
    data = {
        "product_name": [
            "Wireless Earbuds", "Wireless Earbuds", "Wireless Earbuds",
            "Fitness Tracker", "Fitness Tracker", "Fitness Tracker",
            "Smartwatch", "Smartwatch", "Smartwatch"
        ],
        "Price": [2499, 2299, 2399, 1999, 1799, 1899, 4999, 4599, 4799],
        "Discount": [10, 15, 12, 15, 10, 13, 20, 18, 22],
        "Date": [
            "01-01-2025", "02-01-2025", "03-01-2025",
            "06-01-2025", "07-01-2025", "08-01-2025",
            "06-01-2025", "07-01-2025", "08-01-2025"
        ]
    }
    return pd.DataFrame(data)

# Load reviews data
@st.cache_data
def load_reviews_data():
    data = {
    "product_name": [
        "Wireless Earbuds", "Wireless Earbuds", "Wireless Earbuds", "Fitness Tracker",
        "Fitness Tracker", "Fitness Tracker", "Smartwatch", "Smartwatch", "Smartwatch"
    ],
    "Date": pd.to_datetime([
        "28-12-2024", "30-12-2024", "01-01-2025", "29-12-2024", "02-01-2025", "06-01-2025",
        "31-12-2024", "03-01-2025", "06-01-2025"
    ]),
    "reviews": [
        "The earbuds frequently disconnect, and the sound is very muffled.",
        "The sound is average, but the connection issues seem to have improved slightly.",
        "Great sound quality and reliable connection. They are now worth the price.",
        "The step counter is highly inaccurate, and the app keeps crashing.",
        "The tracking has improved after updates, but the app is still buggy.",
        "Accurate tracking, smooth syncing, and a user-friendly app. Very satisfied!",
        "The battery life is poor, and the touchscreen is unresponsive.",
        "The touchscreen works better after the update, but the battery still drains quickly.",
        "The updates fixed all the issues. Excellent battery life and smooth operation now!"
    ]
}

    return pd.DataFrame(data)

# Load data
competitor_data = load_competitor_data()
reviews_data = load_reviews_data()


product_data = competitor_data[competitor_data["product_name"] == selected_product]
product_reviews = reviews_data[reviews_data["product_name"] == selected_product]

st.header(f"Competitor Analysis for {selected_product}")
st.subheader("Competitor Data")
st.table(product_data.tail())

if not product_reviews.empty:
    product_reviews["reviews"] = product_reviews["reviews"].apply(
        lambda x: truncate_text(x, 512)
    )
    reviews = product_reviews["reviews"].tolist()
    sentiments = analyze_sentiment(reviews)

    st.subheader("Customer Sentiment Analysis")
    sentiment_df = pd.DataFrame(sentiments)
    fig = px.bar(sentiment_df, x="label", title="Sentiment Analysis Results")
    st.plotly_chart(fig)
else:
    st.write("No reviews available for this product.")

# Clean and prepare product data for forecasting
product_data["Date"] = pd.to_datetime(product_data["Date"], errors="coerce")
product_data = product_data.dropna(subset=["Date"])
product_data.set_index("Date", inplace=True)
product_data["Discount"] = pd.to_numeric(product_data["Discount"], errors="coerce")
product_data = product_data.dropna(subset=["Discount"])

# Forecasting Model
product_data_with_predictions = forecast_discounts_arima(product_data)

st.subheader("Competitor Current and Predicted Discounts")
st.table(product_data_with_predictions.tail(10))
recommendations = generate_strategy_recommendation(
    selected_product,
    product_data_with_predictions,
    sentiments if not product_reviews.empty else "No reviews available",
)

st.subheader("Strategic Recommendations")
st.write(recommendations)

send_to_slack(recommendations)
