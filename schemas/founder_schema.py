from pydantic import BaseModel, Field


class FounderAnalysis(BaseModel):
    competency_score: int = Field(..., description="Founder competency score on a scale of 1 to 10")
    analysis: str = Field(..., description="Detailed analysis of the founding team, including strengths and challenges.")


class AdvancedFounderAnalysis(FounderAnalysis):
    segmentation: int = Field(..., description="Founder segmentation level (1-5, where 1 is L1, 5 is L5)")
    cosine_similarity: float = Field(..., description="Cosine similarity between founder's desc and startup info")
    idea_fit: float = Field(..., description="Idea fit score")


class FounderSegmentation(BaseModel):
    segmentation: int = Field(..., description="Founder segmentation level (1-5, where 1 is L1, 5 is L5)")