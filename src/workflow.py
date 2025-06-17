from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, InventionInfo, InventionAnalysis
from .firecrawlService import FirecrawlService
from .prompts import ResearcherInventionsPrompts
from urllib.parse import urlparse


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = ResearcherInventionsPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_inventions", self._extract_inventions_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_inventions")
        graph.add_edge("extract_inventions", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()

    def _extract_inventions_step(self, state: ResearchState) -> Dict[str, Any]:
        
        print(f"Searching for articles about: {state.query}")

        article_query = f"{state.query}  + innovation + patent + technology"
        
        search_results, links_found = self.firecrawl.search_links(article_query, num_results=3)

        all_content = ""
        
        print(f"\n\n    Found {len(search_results)} valid URLs results")
        
        for link in links_found:
                        
            url = link
                    
            print(f"WF: Scraping URL:>>{url}<<")
           
            scraped = self.firecrawl.scrape_invention_page(url)
            
            if scraped:
                all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.INVENTIONS_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.inventions_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            invention_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print(f"Extracted inventions: {', '.join(invention_names[:5])}")
            return {"extracted_inventions": invention_names}
        except Exception as e:
            print(e)
            return {"extracted_inventions": []}

    def _analyze_invention_content(self, invention_name: str, content: str) -> InventionAnalysis:
        structured_llm = self.llm.with_structured_output(InventionAnalysis)

        messages = [
            SystemMessage(content=self.prompts.INVENTIONS_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.invention_analysis_user(invention_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            return InventionAnalysis(
                technical_domain="Unknown",
                novelty_features=[],
                maturity_level="Unknown",
                description="Failed",
                implementation_details=[],
                patent_activity=None,
                potential_applications=[],
                ip_protection_notes=None
            )

    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_inventions = getattr(state, "extracted_inventions", [])

        if not extracted_inventions:
            print("-XXX- No extracted inventions found, falling back to direct search")
            search_results, links_found = self.firecrawl.search_links(state.query, num_results=4)
            invention_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results
            ]
        else:
            invention_names = extracted_inventions[:4]

        print(f"Researching specific inventions: {', '.join(invention_names)}")

        inventions = []


        # Iterate over the extracted invention names and search for their official sites
        # If no names were extracted, use the original query

        for name in invention_names:
            search_results, links_found = self.firecrawl.search_links(name + " official site", num_results=1)

            print(f"Searching for official site of: {name}")            

            if search_results:
                result = search_results[0]
                url = links_found[0] 
                
                print(f"Found a link to {name} - Scraping URL:>>--{url}--<<")
                
                invention = InventionInfo(
                    name=name,
                    description=result.get("markdown", ""),
                    website=url,
                    technical_domain=None,
                    novelty_features=[],
                    maturity_level=None,
                    implementation_details=[],
                    patent_activity=None,
                    potential_applications=[],
                    known_competitors=[],
                    ip_protection_notes=None
                )

                if not is_valid_url(url):
                    print(f"Invalid URL for {name}: {url}")
                    continue
                    
                scraped = self.firecrawl.scrape_invention_page(url)
                
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_invention_content(invention.name, content)

                    invention.technical_domain = analysis.technical_domain
                    invention.novelty_features = analysis.novelty_features
                    invention.maturity_level = analysis.maturity_level
                    invention.description = analysis.description
                    invention.implementation_details = analysis.implementation_details
                    invention.patent_activity = analysis.patent_activity
                    invention.potential_applications = analysis.potential_applications
                    invention.ip_protection_notes = analysis.ip_protection_notes

                inventions.append(invention)

        return {"inventions": inventions}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating strategic recommendation")

        invention_data = ", ".join([
            invention.json() for invention in state.inventions
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, invention_data))
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)
