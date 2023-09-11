

import requests

class Bing_Search:

    BING_API_KEY = " "
    BING_NEWS_ENDPOINT = "https://api.bing.microsoft.com/v7.0/news/search"
    BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

    def __init__(self):
        self.headers = {"Ocp-Apim-Subscription-Key": Bing_Search.BING_API_KEY}

    def get_data_from_bing(self, search_query, catg):
        params = {
            "q": search_query, 
            "count": 10, 
            "offset": 0, 
            "mkt": "en-US"
        }
        try:
            if catg == "news":
                response = requests.get(Bing_Search.BING_NEWS_ENDPOINT, headers=self.headers, params=params)
                response.raise_for_status()
                news_data = response.json()
                return news_data.get("value", [])
            if catg == "search":
                response = requests.get(Bing_Search.BING_ENDPOINT, headers=self.headers, params=params)
                response.raise_for_status()
                result_data = response.json()
                return result_data.get("webPages", {}).get("value", [])
            else:
                return []
        except requests.RequestException as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def display_result(search_result, catg):
        if catg == "news":
            for idx, result in enumerate(search_result, 1):
                print(f"{idx}. {result['name']}")
                print(f"   {result['description']}")
                print(f"   {result['url']}\n")
        if catg == "search":
            for idx, result in enumerate(search_result, 1):
                print(f"{idx}. {result['name']}")
                print(f"   {result['snippet']}")
                print(f"   {result['url']}\n")

def main():
    bing_data = Bing_Search()
    
    query = input("Enter the search query for news: ")
    search_result = bing_data.get_data_from_bing(query, "search")
    
    if search_result:
        bing_data.display_result(search_result, "search")
    else:
        print("No results found for the given query.")

if __name__ == "__main__":
    main()


"""
obtaining Bing's Search API key:
> Sign Up for a Microsoft Azure Account
> Access the Azure Portal
> Create a Bing Search Resource
> Get Your API Key
( Bing Search API documentation )
"""


