class ResearcherInventionsPrompts:
    """Collection of prompts for analyzing developer inventions and technologies"""

    # Inventions extraction prompts
    INVENTIONS_EXTRACTION_SYSTEM = """You are a patent research assistant. Extract specific inventions, technologies, tools, or services from articles.
                Focus on actual, identifiable innovations that inventors or patent attorneys might reference in a patent application.
                Exclude general trends or concepts—only include concrete, nameable products, prototypes, or technical solutions."""

    @staticmethod
    def inventions_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific inventions, technologies, or technical solutions mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include concrete, nameable inventions or solutions (no broad ideas or fields)
                - Focus on innovations that could be of interest to inventors or patent attorneys
                - Include both commercialised and prototype-stage technologies
                - Limit to the 5 most relevant inventions or solutions
                - Return only the names or short identifiers, one per line, no descriptions

                Example format:
                Photonic Biosensor Chip
                Multi-Modal Drone Navigation System
                Graphene-Based Water Filter
                Smart Wound Dressing
                Autonomous Soil Analysis Probe"""


    INVENTIONS_ANALYSIS_SYSTEM = """You are analyzing inventions and emerging technologies.
                Focus on extracting information relevant to inventors, patent applicants, and patent attorneys.
                Pay special attention to the technical features, novelty aspects, application areas, and implementation details that may support a patent application.
                Avoid generic marketing language and focus on what makes the technology innovative or unique."""


    @staticmethod
    def invention_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Invention: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from the perspective of an inventor or patent attorney and provide:
                - technical_domain: The main technical field (e.g., biotechnology, robotics, machine learning, medical devices)
                - novelty_features: A short list of novel or inventive aspects claimed or implied in the content
                - maturity_level: One of "Concept", "Prototype", "Production", or "Unknown"
                - description: Brief 1-sentence summary of what the invention does or solves
                - implementation_details: Mention any specific programming languages, hardware platforms, materials, or protocols used
                - patent_activity: true if there is mention of patents, patent applications, or IP protection; false otherwise
                - potential_applications: List of industries or use cases where this invention may apply

                Focus on identifying **technical differentiators, originality, and potential patent relevance**. Do not repeat generic product summaries."""


    RECOMMENDATIONS_SYSTEM = """You are a senior patent analyst providing concise, strategic recommendations to inventors or patent attorneys.
                Keep responses brief and actionable – maximum 3–4 sentences total.
                Focus on technical uniqueness, patentability potential, and application relevance."""


    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Innovation Query: {query}
                Inventions/Technologies Analyzed: {company_data}

                Provide a brief recommendation (3–4 sentences max) covering:
                - Which invention or technology appears most promising and why
                - Potential for patent protection or uniqueness
                - Most relevant application area or industry

                Be concise and direct – no long explanations needed."""


