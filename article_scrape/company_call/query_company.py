import requests
#from bs4 import BeautifulSoup
from newspaper import Article
from requests.exceptions import RequestException
from newspaper.article import ArticleException
bing_api_key = "dd1943ebe53d44c7b0cad1ec3836d972"  # Replace with your actual API key

def get_bing_search_results(query, bing_api_key):
    """Perform a web search using Bing Search API."""
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": query, "count": 4, "offset": 0, "mkt": "en-US"}
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
        article_text =article.text

        # Example: Extract all paragraph texts from the article
        #soup = BeautifulSoup(response.text, 'html.parser')
        #article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return article_text
    
    except RequestException as req_e:
        error_message = f"Network-related error scraping {url}: {req_e}"

    except ArticleException as art_e:
        error_message = f"Error processing article from {url}: {art_e}"

    except Exception as e:
        error_message = f"General error scraping {url}: {e}"

    print(error_message)
    return(error_message)

    #except Exception as e:
    #    return f"Error scraping {url}: {e}"

def main(bing_api_key):

    # Create a search query
    user_input = input("Enter the company you wish to search for: ")
    query = user_input + "battery manufacturing projects europe"

    # Get search results from Bing
    search_results = get_bing_search_results(query, bing_api_key)

    #Scrape articles
    articles = []
    for result in search_results["webPages"]["value"][:4]:
        url = result["url"]
        article_content = scrape_article(url)
        articles.append(article_content)
    return articles, user_input

#Example usage
articles, user_input = main(bing_api_key)

filename = f"{user_input}.txt"
with open(filename, 'w', encoding='utf-8') as file:
   for i, article in enumerate(articles, start=1):
       file.write(f"Article {i}: {article}...\n")
print(f"Results saved in file: {filename}")


#     import os
#     if not os.path.exists(user_input):
#         os.mkdir(user_input)

#     # Scrape and save articles individually
#     for i, result in enumerate(search_results["webPages"]["value"][:4], start=1):
#         url = result["url"]
#         article_content = scrape_article(url)
#         article_filename = f"{user_input}_{i}.txt"
#         with open(os.path.join(user_input, article_filename), 'w', encoding='utf-8') as article_file:
#             article_file.write(article_content)
#         print(f"Article {i} saved in file: {article_filename}")

#     print(f"Results saved in directory: {user_input}")

# # Example usage
# main(bing_api_key)


