import requests
from newspaper import Article
from requests.exceptions import RequestException
from newspaper.article import ArticleException
import os

bing_api_key = "dd1943ebe53d44c7b0cad1ec3836d972"  
return_results_no = 5

projects = ["Tesla Berlin","Verkor Dunkirk","SVOLT Brandenburg"]

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

        article ={
            "title": str(article.title),
            "published_date": str(article.publish_date),
            "keywords": article.keywords,
            "text": str(article.text),
        }
        return article
    
    except RequestException as req_e:
        error_message = f"Network-related error scraping {url}: {req_e}"

    except ArticleException as art_e:
        error_message = f"Error processing article from {url}: {art_e}"

    except Exception as e:
        error_message = f"General error scraping {url}: {e}"

    print(error_message)
    return(error_message)

def main(bing_api_key):

    # Create a search query
    #user_input = input("Enter the project you wish to search for: ")
    query = project + "battery manufacturing project latest"

    # Get search results from Bing
    search_results = get_bing_search_results(query, bing_api_key)

    #Scrape articles
    articles = []
    for result in search_results["webPages"]["value"][:6]:
        url = result["url"]
        article_content = scrape_article(url)
        articles.append(article_content)
    return articles

# call function
for project in projects:

    articles = main(bing_api_key)

    folder_path = 'data/output/project'
    filename = os.path.join(folder_path, f"{project}.txt")

    with open(filename, 'w', encoding='utf-8') as file:
        for i, article in enumerate(articles, start=1):
            file.write(f"Article {i}: {article}...\n")
    print(f"Results saved in file: {filename}")



