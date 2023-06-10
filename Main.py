import requests
import random
import json
from pathlib import Path
from hashlib import sha256

# Create directory for storing wallet data
wallet_dir = Path("wallet")
wallet_dir.mkdir(exist_ok=True)

# Create directory for storing news article data
news_dir = Path("news_articles")
news_dir.mkdir(exist_ok=True)

# Create directory for storing sponsored content
sponsor_dir = Path("sponsored_content")
sponsor_dir.mkdir(exist_ok=True)

# Function to fetch trending news
def fetch_trending_news(api_key, country="us", categories=["technology", "science", "business", "world"], page_size=10):
    base_url = "https://newsapi.org/v2/top-headlines"
    news_url = f"{base_url}?country={country}&pageSize={page_size}&apiKey={api_key}"

    news = []
    for category in categories:
        url = f"{news_url}&category={category}"
        response = requests.get(url)

        if response.status_code == 200:
            articles = response.json()["articles"]
            for article in articles:
                # Generate a unique URL for each article
                article_hash = sha256(article['url'].encode()).hexdigest()
                article["proof_of_work_url"] = f"https://tenwolfproof.com/proofofwork/{article_hash}"

                # Save the news article URL
                article["news_url"] = article["url"]

                # Save news article data to a file
                filename = f"news_{len(news)}.json"
                filepath = news_dir / filename
                with open(filepath, "w") as f:
                    json.dump(article, f, indent=4)

                news.append(article)
        else:
            print(f"Error fetching {category} news data:", response.status_code)

    return {"articles": news[:page_size]}


# Function to add sponsor content
def add_sponsor_content(title, content):
    sponsor_data = {"title": title, "content": content}

    # Save sponsor content to a file
    filename = f"sponsor_{len(list(sponsor_dir.glob('*.json')))}.json"
    filepath = sponsor_dir / filename
    with open(filepath, "w") as f:
        json.dump(sponsor_data, f, indent=4)


# Function to add advertising content
def add_advertising_content(title, content):
    advertising_data = {"title": title, "content": content}

    # Save advertising content to a file
    filename = f"advertising_{len(list(sponsor_dir.glob('*.json')))}.json"
    filepath = sponsor_dir / filename
    with open(filepath, "w") as f:
        json.dump(advertising_data, f, indent=4)


# Your API key from News API
api_key = "822b36ed92ab4eb798e10e5353af44fd"

# Fetch trending news
trending_news = fetch_trending_news(api_key)

if trending_news:
    # Process and display news
    for i, news_item in enumerate(trending_news["articles"]):
        title = news_item["title"]
        description = news_item["description"]
        news_url = news_item["url"]
        print(f"{i+1}. {title}")
        print(description)
        print(f"Read more: {news_url}")
        print(f"Visit TenWolf: [tenwolf.com]({news_url})")
        print()

        # Prompt user for rating and feedback
        rating = input("Please rate this article (1-5): ")
        feedback = input("Please provide your feedback: ")

        # Generate unique token for the user
        token = random.randint(100, 99999)

                # Save the user's information with the generated token
        user_info = {"rating": rating, "feedback": feedback, "token": token}

        # Prompt user if they want to sponsor the article
        sponsor_choice = input("Do you want to sponsor this article? (yes/no): ")
        if sponsor_choice.lower() == "yes":
            sponsor_title = input("Enter the sponsor title: ")
            sponsor_content = input("Enter the sponsor content: ")
            add_sponsor_content(sponsor_title, sponsor_content)

        # Prompt user if they want to add advertising content
        advertising_choice = input("Do you want to add advertising content? (yes/no): ")
        if advertising_choice.lower() == "yes":
            advertising_title = input("Enter the advertising title: ")
            advertising_content = input("Enter the advertising content: ")
            add_advertising_content(advertising_title, advertising_content)

        print("-" * 40)

        # Print the user's information
        print("Thank you for using TenWolf! Here's your User Information:")
        print(f"Rating: {rating}")
        print(f"Feedback: {feedback}")
        print(f"Token: {token}")

        # Tip Jar
        print("Tip Jar: If you found this program helpful, consider leaving a tip!")
        print("Bitcoin Address: bc1q2rx794nvtnzjg45csa806cecxvl5zl7dzrtx3p")
        print("Ethereum Address: 0x8eb8d3E755F92767D021282a44CFBD85649c4430")
