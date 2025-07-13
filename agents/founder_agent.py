import os
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import load_model

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from shared.types import StartupInfo

from agents.base_agent import BaseAgent
from schemas.founder_schema import FounderAnalysis, AdvancedFounderAnalysis, FounderSegmentation
from prompts.founder_prompt import ANALYSIS_PROMPT, SEGMENTATION_PROMPT

class FounderAgent(BaseAgent):
    def __init__(self, model="gpt-4o"):
        super().__init__(model)
        try:
            self.neural_network = load_model(os.path.join(project_root, 'models', 'neural_network.keras'))
        except Exception as e:
            print(f"Warning: Could not load neural network model: {e}")
            print("The founder agent will continue without neural network support.")
            self.neural_network = None

    def analyze(
        self,
        startup_info: StartupInfo, 
        mode: str,
    ) -> FounderAnalysis | AdvancedFounderAnalysis:
        founder_info = self._get_founder_info(startup_info)
        
        if mode == "advanced":
            basic_analysis = self.get_json_response(FounderAnalysis, ANALYSIS_PROMPT, founder_info)
            segmentation = self.segment_founder(founder_info)
            idea_fit, cosine_similarity = self.calculate_idea_fit(startup_info, founder_info)
            
            return AdvancedFounderAnalysis(
                **basic_analysis.model_dump(),
                segmentation=segmentation,
                cosine_similarity=cosine_similarity,
                idea_fit=idea_fit,
            )
        else:
            return self.get_json_response(FounderAnalysis, ANALYSIS_PROMPT, founder_info)

    def _get_founder_info(self, startup_info: StartupInfo) -> str:
        return f"Founders' Backgrounds: {startup_info.get('founder_backgrounds', '')}\n" \
               f"Track Records: {startup_info.get('track_records', '')}\n" \
               f"Leadership Skills: {startup_info.get('leadership_skills', '')}\n" \
               f"Vision and Alignment: {startup_info.get('vision_alignment', '')}"

    def segment_founder(self, founder_info: str) -> FounderSegmentation:
        return self.get_json_response(FounderSegmentation, SEGMENTATION_PROMPT, founder_info).segmentation

    def calculate_idea_fit(
        self,
        startup_info: StartupInfo,
        founder_info: str
    ) -> tuple[float, float]:
        founder_embedding = self.openai_api.get_embeddings(founder_info)
        startup_embedding = self.openai_api.get_embeddings(startup_info['description'])
        cosine_sim = self._calculate_cosine_similarity(founder_embedding, startup_embedding)
        
        # Prepare input for neural network
        X_new_embeddings = np.array(founder_embedding).reshape(1, -1)
        X_new_embeddings_2 = np.array(startup_embedding).reshape(1, -1)
        X_new_cosine = np.array([[cosine_sim]])
        X_new = np.concatenate([X_new_embeddings, X_new_embeddings_2, X_new_cosine], axis=1)

        # Predict using the neural network
        if self.neural_network is not None:
            idea_fit = self.neural_network.predict(X_new)[0][0]
        else:
            # Fallback: use cosine similarity as a simple approximation
            idea_fit = cosine_sim
        return float(idea_fit), cosine_sim

    def _calculate_cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        vec1 = np.array(vec1).reshape(1, -1)
        vec2 = np.array(vec2).reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]


if __name__ == "__main__":
    def test_founder_agent():
        # Create a FounderAgent instance
        agent = FounderAgent()

        # Test startup info
        startup_info = {
            "founder_backgrounds": "MBA from Stanford, 5 years at Google as Product Manager",
            "track_records": "Successfully launched two products at Google, one reaching 1M users",
            "leadership_skills": "Led a team of 10 engineers and designers",
            "vision_alignment": "Strong passion for AI and its applications in healthcare",
            "description": "AI-powered health monitoring wearable device"
        }

        # Test basic analysis
        print("Basic Analysis:")
        basic_analysis = agent.analyze(startup_info, mode="basic")
        print(basic_analysis)
        print()

        # Test advanced analysis
        print("Advanced Analysis:")
        advanced_analysis = agent.analyze(startup_info, mode="advanced")
        print(advanced_analysis)

    # Run the test function
    test_founder_agent()
