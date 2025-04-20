import requests

API_KEY = "your_news_api_key_here"  # Replace with your News API key

def get_news(city):
    url = "https://newsdata.io/api/1/news"
    params = {
        'apikey': API_KEY,
        'q': city,
        'language': 'en',
        'category': 'top'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("results", [])
        if not articles:
            return {"error": f"No news found for {city}."}

        headlines = [article["title"] for article in articles[:5]]
        return {
            "city": city,
            "headlines": headlines
        }
    else:
        return {"error": "Failed to fetch news data."}
