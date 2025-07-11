import os
import sys
import logging
import joblib
import pandas as pd
from typing import Tuple

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from agents.base_agent import BaseAgent
from schemas.vc_scout_schema import StartupInfo, StartupCategorization, StartupEvaluation
from prompts.vc_scout_prompt import (
    PARSE_RECORD_PROMPT,
    BASIC_EVALUATION_PROMPT,
    ADVANCED_EVALUATION_PROMPT,
    CATEGORIZATION_PROMPT
)

class VCScoutAgent(BaseAgent):
    def __init__(self, model="gpt-4o-mini"):
        super().__init__(model)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Load the encoder and model
        self.encoder = joblib.load(os.path.join(project_root, 'models/trained_encoder_RF.joblib'))
        self.model_random_forest = joblib.load(os.path.join(project_root,'models/random_forest_classifier.joblib'))

    def parse_record(self, startup_info: str) -> StartupInfo:
        """
        Convert a string description of a startup into a StartupInfo schema.
        """
        self.logger.info("Parsing startup information into StartupInfo schema")
        prompt = PARSE_RECORD_PROMPT  
        try:
            startup_info_dict = self.get_json_response(StartupInfo, prompt, startup_info)
            self.logger.debug(f"Parsed startup info: {startup_info_dict}")
            return startup_info_dict  # Return the dictionary directly
        except Exception as e:
            self.logger.error(f"Error parsing startup info: {str(e)}")
            return StartupInfo(name="Error", description="Failed to parse startup info")

    def evaluate(self, startup_info: StartupInfo, mode: str) -> StartupEvaluation:
        self.logger.info(f"Starting startup evaluation in {mode} mode")
        startup_info_str = startup_info.json()
        self.logger.debug(f"Startup info: {startup_info_str}")
        
        if mode == "basic":
            analysis = self.get_json_response(StartupEvaluation, BASIC_EVALUATION_PROMPT, startup_info_str)
            self.logger.info("Basic evaluation completed")
        else:  # advanced mode
            analysis = self.get_json_response(StartupEvaluation, ADVANCED_EVALUATION_PROMPT, startup_info_str)
            self.logger.info("Advanced evaluation completed")
        
        return analysis

    def side_evaluate(self, startup_info: StartupInfo) -> Tuple[str, StartupCategorization]:
        self.logger.info("Starting side evaluation")
        startup_info_str = startup_info.json()
        categorization = self.get_json_response(StartupCategorization, CATEGORIZATION_PROMPT, startup_info_str)
        self.logger.info("Categorization completed")

        # Validate the categorization
        # for field, value in categorization:
        #     expected_values = StartupCategorization.__fields__[field].field_info.description.split('[')[1].split(']')[0].split('/')
        #     if value not in expected_values:
        #         self.logger.warning(f"Unexpected value '{value}' for field '{field}'. Expected one of {expected_values}. Setting to 'N/A'.")
        #         setattr(categorization, field, 'N/A')

        prediction = self._predict(categorization)
        self.logger.info(f"Prediction: {prediction}")

        return prediction, categorization

    def _predict(self, categorization: StartupCategorization) -> str:
        category_mappings = {
            "industry_growth": ["No", "N/A", "Yes"],
            "market_size": ["Small", "Medium", "Large", "N/A"],
            "development_pace": ["Slower", "Same", "Faster", "N/A"],
            "market_adaptability": ["Not Adaptable", "Somewhat Adaptable", "Very Adaptable", "N/A"],
            "execution_capabilities": ["Poor", "Average", "Excellent", "N/A"],
            "funding_amount": ["Below Average", "Average", "Above Average", "N/A"],
            "valuation_change": ["Decreased", "Remained Stable", "Increased", "N/A"],
            "investor_backing": ["Unknown", "Recognized", "Highly Regarded", "N/A"],
            "reviews_testimonials": ["Negative", "Mixed", "Positive", "N/A"],
            "product_market_fit": ["Weak", "Moderate", "Strong", "N/A"],
            "sentiment_analysis": ["Negative", "Neutral", "Positive", "N/A"],
            "innovation_mentions": ["Rarely", "Sometimes", "Often", "N/A"],
            "cutting_edge_technology": ["No", "Mentioned", "Emphasized", "N/A"],
            "timing": ["Too Early", "Just Right", "Too Late", "N/A"]
        }

        feature_order = list(category_mappings.keys())
        encoded_features = self.encoder.transform(pd.DataFrame([categorization.dict()]))
        prediction = self.model_random_forest.predict(encoded_features)

        return "Successful" if prediction[0] == 1 else "Unsuccessful"


if __name__ == "__main__":
    def test_vc_scout_agent():
        # Configure logging for the test function
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        logger.info("Starting VCScoutAgent test")
        # Create a VCScoutAgent instance
        agent = VCScoutAgent()

        # Test startup info
        startup_info_str = """
        HealthTech AI is developing an AI-powered health monitoring wearable device. 
        The global wearable technology market is estimated at $50 billion with a CAGR of 15.9% from 2020 to 2027. 
        Key competitors include Fitbit, Apple Watch, and Garmin. 
        The product offers real-time health tracking with predictive analysis. 
        The founding team consists of experienced entrepreneurs with backgrounds in AI and healthcare. 
        They've raised $2 million in seed funding to date.
        """

        # Test parse_record
        print("Parsing Startup Info:")
        startup_info = agent.parse_record(startup_info_str)
        print(startup_info)
        print()

        # Test basic evaluation
        print("Basic Evaluation:")
        basic_evaluation = agent.evaluate(startup_info, mode="basic")
        print(basic_evaluation)
        print()

        # Test advanced evaluation
        print("Advanced Evaluation:")
        advanced_evaluation = agent.evaluate(startup_info, mode="advanced")
        print(advanced_evaluation)
        print()

        # Test side evaluation
        print("Side Evaluation:")
        prediction, categorization = agent.side_evaluate(startup_info)
        print(f"Prediction: {prediction}")
        print("Categorization:")
        print(categorization)

    # Run the test function
    test_vc_scout_agent()
