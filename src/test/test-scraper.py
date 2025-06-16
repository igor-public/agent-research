from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
import json

load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../local.env")))


class Scraper:
    def __init__(self):
        self.app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    def scrape_invention_page(self, url: str):
        try:
            result = self.app.scrape_url(
                url, formats=["markdown"]
            )
            return result
        except Exception as e:
            print(f"[Firecrawl Scrape Error] {e}")
            return None


def main():
    url = "https://patents.google.com/patent/EP4227276A1/en"
    scraper = Scraper()
    result = scraper.scrape_invention_page(url)
    if result:
        print("\n[Scraped Result]\n")
        print(result)
    else:
        print("No content returned.")


if __name__ == "__main__":
    main()
