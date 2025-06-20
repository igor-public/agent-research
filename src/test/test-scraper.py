from firecrawl import FirecrawlApp
from firecrawlService import firecrawlService as fc
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../local.env")))

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url.strip())
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False

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
    
    print("Scraper Test")
    
    fc.search_links("Electric Vehicle Battery Management Systems innovation patent technology", 5) 
  
    
    
    """ scraper = Scraper()
    result = scraper.scrape_invention_page(url)
    if result:
        print("\n[Scraped Result]\n")
        print(result)
    else:
        print("No content returned.") """


if __name__ == "__main__":
    main()
