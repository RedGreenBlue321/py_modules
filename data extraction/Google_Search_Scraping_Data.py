

import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import random

class GoogleScraper:
    USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    def __init__(self, query, num_results=10):
        self.query = query
        self.num_results = num_results

    def fetch_search_results(self):
        search_results = []
        headers = {
            'User-Agent': self.USER_AGENT
        }

        for url in search(self.query, num_results=self.num_results):
            result = self._get_page_content(url, headers)
            if result:
                search_results.append(result)
            self._delay_time()

        return search_results

    def _get_page_content(self, url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
             
            title = soup.title.string if soup.title else "No Title"
             
            # Extracting snippets can be challenging since websites have varied structures.
            # This will attempt to get a general description or fallback to the first p tag.
            snippet = soup.find('meta', attrs={'name': 'description'}) or soup.find('p')
            snippet_text = snippet.get('content') if snippet and snippet.get('content') else (snippet.text if snippet else "No snippet available")
            
            if len(snippet_text) > 300:  # Limiting snippet length to 300 characters
                snippet_text = snippet_text[:297] + "..."
            """
                        
            paragraphs = soup.find_all('p')
            content = ' '.join([p.text for p in paragraphs if p.text])  
            """
            return {
                'title': title,
                'link': url,
                'snippet': snippet_text
#                'content': content
            }

        except requests.RequestException as e:
            print(f"Error fetching details for {url}. Reason: {e}")
            return None

    def _delay_time(self):
        time.sleep(random.uniform(1, 3))  # Random sleep between 1 and 3 seconds

if __name__ == '__main__':
    query = input("Enter your search query: ")
    scraper = GoogleScraper(query)
    results = scraper.fetch_search_results()

    for res in results:
        print("Title:", res['title'])
        print("Link:", res['link'])
        print("Snippet:", res['snippet'])
#        print("Content:", res['content'])
        print('-' * 30)

