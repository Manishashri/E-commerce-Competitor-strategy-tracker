# Real-Time Competitor Strategy Tracker for E-Commerce

## 1. Project Overview
The **Real-Time Competitor Strategy Tracker** is an advanced e-commerce monitoring tool that helps businesses track competitor pricing, discounts, and customer sentiment. By leveraging web scraping, predictive analytics, and AI-powered sentiment analysis, this tool provides strategic insights for businesses to stay ahead in the market.

## 2. Features
- **Real-Time Data Scraping**: Extracts product prices, discounts, and ratings from e-commerce websites.
- **Sentiment Analysis**: Analyzes customer reviews using an NLP model to determine sentiment trends.
- **Predictive Pricing Model**: Uses ARIMA and Random Forest models to forecast competitor discounts.
- **Slack Notifications**: Sends strategic recommendations directly to a Slack channel.
- **Interactive Dashboard**: Built with Streamlit and Plotly for data visualization and business insights.

## 3. Setup Instructions

### Step 1: Install Dependencies
Ensure you have Python installed and install the required libraries:
```sh
pip install -r requirements.txt
```

### Step 2: Set Up Groq API Key
Obtain a Groq API Key and add it to your environment variables:
```sh
export API_KEY="your_groq_api_key"
```

### Step 3: Configure Slack Webhook
Set up a Slack Webhook to receive notifications:
```sh
export SLACK_WEBHOOK="your_slack_webhook_url"
```

### Step 4: Run the Scraper
Run the scraper to collect competitor data:
```sh
python scrape.py
```

### Step 5: Start the Dashboard
Launch the Streamlit dashboard:
```sh
streamlit run app.py
```

## 4. Project Files
- **app.py**: Streamlit dashboard for visualizing competitor data.
- **scrape.py**: Web scraper for collecting product details from e-commerce sites.
- **competitor_data.csv**: Stores scraped competitor data.
- **reviews.csv**: Stores collected customer reviews.
- **requirements.txt**: List of required Python dependencies.
- **readme.md**: Documentation for the project.

## 5. Usage
1. Run `scrape.py` to gather competitor data from e-commerce websites.
2. Start the `app.py` dashboard to analyze real-time insights.
3. View predicted pricing trends and sentiment analysis.
4. Receive strategic recommendations and notifications via Slack.

---

