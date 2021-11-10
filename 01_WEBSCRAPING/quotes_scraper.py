import pandas as pd
import time
import pyfiglet
from fx_quotes_scraper_template import *

def main() -> None:
    """
    This function loops through all the page links to scrape data
    """
    
    page_url = "https://quotes.toscrape.com/page/1/"
    
    while True:
        
        print(f'Scraping Page URL: {page_url}')
        
        content = extract_content(page_url)
        scrape_content(content)
        time.sleep(0.5)
        
        print(f'Total Quotes Collected: {len(all_quotes)}')
        print('\n')
        
        if extract_nextpage_link(page_url) == None:
            break
        else:
            next_page_link = extract_nextpage_link(page_url)
            page_url = next_page_link

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    quotes_df = pd.DataFrame(all_quotes)
    quotes_df.to_csv('quotes_data.csv', index=False)

if __name__ == '__main__':
    
    scraper_title = "QUOTES COLLECTOR"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    print('\n\n')
    print(ascii_art_title)
    print('Collecting Quotes...')
    
    start_time = datetime.datetime.now()
    
    main()
    
    end_time = datetime.datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All Quotes Collected...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total quotes collected: {len(all_quotes)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping completed !!!')