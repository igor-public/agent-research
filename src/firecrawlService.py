import os
import requests
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv("local.env")


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url.strip())
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        print(f"[URL Validation Error] Invalid URL: {url}")
        return False


class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_links_firecrawl(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} innovation patent technology",
                limit=num_results,
                scrape_options=ScrapeOptions(formats=["markdown"]),
            )
            return result
        except Exception as e:
            print(f"[Firecrawl Search Error] {e}")
            return []

    # Using Serper API for search
    # This method searches for inventions using the Serper API and returns a list of results.
    # Each result contains title, URL, snippet, etc.
    # It also validates URLs and removes any invalid ones from the results.

    def search_links(self, query: str, num_results: int = 5) -> tuple[list[dict], list[str]]:
        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": os.getenv("SERPER_API_KEY")},
                json={"q": f"{query} + innovation + patent + technology"},
            )

            results = response.json().get("organic", [])[:num_results]

            # Get links only and Strip whitespace from them

            links = []

            links[:] = map(lambda x: x.get("link", "").strip(), results)
            print(f"[Search] {len(links)} link(s) found for query: {query}")

            for link in links:
                print(f"[Search] *** Found link: --{link}--")

            print(flush=True)

            # Filter out invalid URLs

            links = [link for link in links if is_valid_url(link)]
            print(f"[Search] {len(links)} are valid link(s)")

            print(f"[Search] {len(links)} valid link(s) found for query: {query}")
            print(flush=True)

            for link in links:
                print(f"[Search] +++ Found link: --{link}--")

            
            return results, links

        except Exception as e:
            print(f"[Serper Search Error] {e}")
            return [],[]


    def scrape_invention_page(self, url: str):
        try:
            url = url.strip()

            print(f"[Firecrawl Scrape] Scraping URL: --{url}--")
            result = self.app.scrape_url(url, formats=["markdown"])
            return result

        except Exception as e:
            print(f"[Firecrawl Scrape Error] {e}")
            return None
