import os
import requests
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv("local.env")

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_inventions_old(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} innovation patent technology",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(f"[Firecrawl Search Error] {e}")
            return []


    def search_inventions(self, query: str, num_results: int = 5):
        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": os.getenv("SERPER_API_KEY")},
                json={"q": f"{query} innovation patent technology"}
            )
            results = response.json().get("organic", [])[:num_results]
            #print (f"[Serper Search] Found {len(results)} result(s) for query: {query}")
            
            """             for result in results:
                if is_valid_url(result.get("link", "")):
                    print(f"[Serper Search] the URL found: {result.get('link', '')}")
 """            
            for result in results:
                if not is_valid_url(result.get("link", "")):
                    print(f"[Serper Search] Invalid URL found: {result.get('link', '')}")
                    results.remove(result)
                    continue
                print(f"[Serper Search] Valid URL found: {result.get('link', '')}")
                       
            return results  # each result has title, url, snippet, etc.
        except Exception as e:
            print(f"[Serper Search Error] {e}")
            return []



    def scrape_invention_page(self, url: str):
        
        try:
            print(f"[Firecrawl Scrape] Scraping URL: --{url.strip()}--")
            result = self.app.scrape_url(
                url.strip(),
                formats=["markdown"]
            )
            return result
        
        except Exception as e:
                print(f"[Firecrawl Scrape Error] {e}")
                return None
