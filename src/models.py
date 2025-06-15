from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class InventionAnalysis(BaseModel):
    technical_domain: str  # e.g., AI, MedTech, Robotics
    novelty_features: List[str] = []
    maturity_level: str  # Concept, Prototype, Production, Unknown
    description: str = ""  # Short summary of what the invention solves
    implementation_details: List[str] = []  # Programming languages, hardware, materials
    patent_activity: Optional[bool] = None  # Whether patent/IP protection is mentioned
    potential_applications: List[str] = []  # Target industries or use cases
    ip_protection_notes: Optional[str] = None  # e.g., "EU patent granted", "USPTO filing in progress"



class InventionInfo(BaseModel):
    name: str
    description: str
    website: str
    technical_domain: Optional[str] = None  # robotics, bioinformatics
    novelty_features: List[str] = []
    maturity_level: Optional[str] = None  # Concept, Prototype, Production, Unknown
    implementation_details: List[str] = []  # languages, materials, hardware, protocols
    patent_activity: Optional[bool] = None  # True/False if IP or patent is mentioned
    potential_applications: List[str] = []  # e.g., healthcare, logistics
    known_competitors: List[str] = []
    ip_protection_notes: Optional[str] = None  # e.g., "PCT filed", "Patent pending"



class ResearchState(BaseModel):
    query: str
    extracted_inventions: List[str] = []  # Inventions/technologies extracted from content
    inventions: List[InventionInfo] = []  # Detailed invention metadata
    search_results: List[Dict[str, Any]] = []  # Raw search result data
    analysis: Optional[str] = None  # Summary recommendation
