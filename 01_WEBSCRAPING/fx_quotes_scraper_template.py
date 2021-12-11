import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

SESSION = requests.Session()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "accept-language": "en-US"
}

all_quotes = []

def extract_content(page_url: str) -> str:
    """
    This function takes the page URL as an input and returns the HTML content that has all the quotes and their related attributes from that page.
    Args:
        page_url (str): The page URL
    Returns:
        str: HTML content only having the quotes and related details 
    """
    response = SESSION.get(page_url, headers=HEADERS)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    content = soup.find_all('div', class_ = 'quote')
    return content

def scrape_content(content: str) -> None:   
    """
    This functions takes the HTML content of a specific page URL as an input argument; scrapes the quotes along with their related attributes and stores it in 'all_books' list

    Args:
        content (str): The HTML content having the quotes and their related attributes from a specific page
    Returns:
        None: This function returns nothing but adds the scraped content into 'all_books' list
    """
    
    utc_timezone = timezone.utc
    current_utc_timestamp = datetime.now(utc_timezone).strftime('%d-%b-%Y %H:%M:%S')

    for item in content:
        quote = item.find('span', class_='text').text
        author = item.find('small', class_ = 'author').text
        tags = item.find('meta', class_ = 'keywords')['content']

        quote_details = {
            "quote": quote,
            "author": author,
            "tags": tags,
            "last_updated_at_UTC": current_utc_timestamp
        }

        all_quotes.append(quote_details)
    return

def extract_nextpage_link(page_url: str) -> str:
    """
    This function checks whether the "next page" button is present in the webpage or, not and returns the value accordingly.
    Args:
        page_url (str): This is the input page URL
    Returns:
        str: next page URL; if it exists, otherwise, the function will return "None"
    """

    root_url = "https://quotes.toscrape.com/"
    
    response = SESSION.get(page_url, headers=HEADERS)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    if soup.find('li', class_= 'next') is not None:
        next_page_partial_link = soup.find('li', class_= 'next').find('a')['href']
        next_page_link = urljoin(root_url, next_page_partial_link)
    else:
        next_page_link = None
    return next_page_link

# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':
    
    page_url = "https://quotes.toscrape.com/page/1/"
    
    print('\n')
    print(f'Page URL to scrape: {page_url}')
    print('\n')
    
    content = extract_content(page_url)
    scrape_content(content)
    
    print('\n')
    print(f'Total quotes scraped: {len(all_quotes)}')
    print('\n')
    print(all_quotes)
    
    print('\n')
    print(f"Does next page exists? : {extract_nextpage_link(page_url) != None}")
    print('\n')
    print(f"Next Page URL: {extract_nextpage_link(page_url) }")