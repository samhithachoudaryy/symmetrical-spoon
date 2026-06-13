```python
import streamlit as st
import requests
import pandas as pd

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Advanced News Aggregator",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Advanced News Aggregator")
st.markdown("Fetch and filter news articles using NewsAPI")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("News Filters")

api_key = st.sidebar.text_input(
    "Enter NewsAPI Key",
    type="password"
)

country = st.sidebar.selectbox(
    "Location (Country)",
    {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Australia": "au",
        "Canada": "ca",
        "Germany": "de",
        "France": "fr"
    }
)

category = st.sidebar.selectbox(
    "Topic",
    [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, Tesla, Cricket..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=100,
    value=20
)

# ----------------------------
# Fetch News Function
# ----------------------------
def fetch_news(api_key, country_code, category, keyword, page_size):
    base_url = "https://newsapi.org/v2/top-headlines"

    params = {
        "apiKey": api_key,
        "country": country_code,
        "category": category,
        "pageSize": page_size
    }

    if keyword:
        params["q"] = keyword

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None


# ----------------------------
# Main Section
# ----------------------------
if st.button("Fetch News"):

    if not api_key:
        st.warning("Please enter your NewsAPI key.")
        st.stop()

    with st.spinner("Fetching latest news..."):
        news_data = fetch_news(
            api_key,
            country,
            category,
            keyword,
            article_count
        )

    if news_data and news_data.get("articles"):

        articles = news_data["articles"]

        st.success(f"Found {len(articles)} articles")

        article_records = []

        for article in articles:

            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown")
            description = article.get("description", "")
            url = article.get("url", "")
            image = article.get("urlToImage")
            published = article.get("publishedAt")

            article_records.append({
                "Title": title,
                "Source": source,
                "Published": published,
                "URL": url
            })

            with st.container():

                col1, col2 = st.columns([1, 3])

                with col1:
                    if image:
                        st.image(image, use_container_width=True)

                with col2:
                    st.subheader(title)
                    st.write(f"**Source:** {source}")
                    st.write(f"**Published:** {published}")

                    if description:
                        st.write(description)

                    st.markdown(
                        f"[Read Full Article]({url})"
                    )

                st.divider()

        # ----------------------------
        # Download CSV
        # ----------------------------
        df = pd.DataFrame(article_records)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Articles CSV",
            data=csv,
            file_name="news_articles.csv",
            mime="text/csv"
        )

        # ----------------------------
        # Data Table
        # ----------------------------
        st.subheader("News Summary Table")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No articles found.")
```
