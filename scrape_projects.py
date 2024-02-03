import requests
from newspaper import Article
from requests.exceptions import RequestException
from newspaper.article import ArticleException
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import pandas as pd
import re
load_dotenv()

bing_api_key = os.getenv("BING_API_KEY")
return_results_no = 8
tech = 'battery'

df = pd.read_excel('data/input/projects.xlsx')
projects = df[tech].tolist()

def get_bing_search_results(query, bing_api_key):
    """Perform a web search using Bing Search API."""
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": query, "count": return_results_no, "offset": 0, "mkt": "en-US"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    return response.json()

def scrape_article(url):
    """Scrape the content of an article given its URL."""
    try:
        # headers make the bot look more like a real person supposedly
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=15)

        article = Article(url)
        article.download(input_html=response.text)
        article.parse()

        # Initial date from newspaper
        publish_date = article.publish_date

        # Fallback using BeautifulSoup if newspaper fails
        if not publish_date:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Example: Look for a <meta> tag with the publish date
            meta_date = soup.find('meta', {'property': 'article:published_time'})
            if meta_date:
                publish_date = meta_date.get('content')

            # Additional fallback: search with regex in HTML or article text
            if not publish_date:
                date_pattern = r'\d{4}-\d{2}-\d{2}'  # Adjust regex pattern as needed
                match = re.search(date_pattern, response.text)
                if match:
                    publish_date = match.group()

        return {
        'title': article.title,
        'url':url,
        'date': publish_date,
        'text': article.text
        }
    
    except RequestException as req_e:
        error_message = f"Network-related error scraping {url}: {req_e}"

    except ArticleException as art_e:
        error_message = f"Error processing article from {url}: {art_e}"

    except Exception as e:
        error_message = f"General error scraping {url}: {e}"

    print(error_message)
    return None

for project in projects:
    articles_data = []
    query = project + f" {tech} manufacturing project investment"
    print(query)
    search_results = get_bing_search_results(query, bing_api_key)

    for result in search_results["webPages"]["value"]:
        url = result["url"]  
        article_data = scrape_article(url)
        if article_data is not None:
            articles_data.append(article_data)

    df = pd.DataFrame(articles_data)

    directory = f'data/output/project/{tech}/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{project}.csv"
    file_path = os.path.join(directory, filename)

    df.to_csv(file_path, index=False)