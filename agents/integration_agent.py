import os
import sys
import logging

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from agents.base_agent import BaseAgent
from schemas.integration_schema import IntegratedAnalysis, QuantitativeDecision
from prompts.integration_prompt import BASIC_INTEGRATION_PROMPT, PRO_INTEGRATION_PROMPT, QUANT_DECISION_PROMPT

class IntegrationAgent(BaseAgent):
    def __init__(self, model="gpt-4o"):
        super().__init__(model)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def integrated_analysis_basic(
        self,
        market_info,
        product_info,
        founder_info
    ):
        self.logger.info("Starting basic integrated analysis")
        
        user_prompt = BASIC_INTEGRATION_PROMPT.format(
            market_info=market_info,
            product_info=product_info,
            founder_info=founder_info
        )
        
        integrated_analysis = self.get_json_response(IntegratedAnalysis, user_prompt, "Be professional.")
        self.logger.info("Basic integrated analysis completed")
        
        return integrated_analysis

    def integrated_analysis_pro(
        self,
        market_info,
        product_info,
        founder_info,
        founder_idea_fit,
        founder_segmentation,
        rf_prediction
    ):
        self.logger.info("Starting pro integrated analysis")
        
        user_prompt = PRO_INTEGRATION_PROMPT.format(
            market_info=market_info,
            product_info=product_info,
            founder_info=founder_info,
            founder_idea_fit=founder_idea_fit,
            founder_segmentation=founder_segmentation,
            rf_prediction=rf_prediction
        )
        
        integrated_analysis = self.get_json_response(IntegratedAnalysis, user_prompt, "Be professional.")
        self.logger.info("Pro integrated analysis completed")
        
        return integrated_analysis

    def getquantDecision(
        self,
        rf_prediction,
        Founder_Idea_Fit,
        Founder_Segmentation
    ):
        self.logger.info("Starting quantitative decision analysis")
        
        user_prompt = f"You are provided with the categorical prediction outcome of {rf_prediction}, Founder Segmentation of {Founder_Segmentation}, Founder-Idea Fit of {Founder_Idea_Fit}."

        quant_decision = self.get_json_response(QuantitativeDecision, QUANT_DECISION_PROMPT, user_prompt)
        self.logger.info("Quantitative decision analysis completed")
        
        return quant_decision

if __name__ == "__main__":
    def test_integration_agent():
        # Configure logging for the test function
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        logger.info("Starting IntegrationAgent test")
        # Create an IntegrationAgent instance
        agent = IntegrationAgent()

        # Test market info
        market_info = """
        Market size: $50 billion global wearable technology market
        Growth rate: CAGR of 15.9% from 2020 to 2027
        Competition: Fitbit, Apple Watch, Garmin
        Market trends: Increasing health consciousness, integration of AI in healthcare
        Viability score: 8
        """

        # Test product info
        product_info = """
        Features analysis: Real-time health tracking with predictive analysis
        Tech stack evaluation: IoT sensors, Machine Learning algorithms, Cloud computing
        USP assessment: Predictive health analysis with medical-grade accuracy
        Potential score: 9
        Innovation score: 8
        Market fit score: 7
        """

        # Test founder info
        founder_info = """
        Competency score: 8
        Strengths: Strong technical background, previous startup experience
        Challenges: Limited experience in the healthcare industry
        Segmentation: L4
        Idea fit: 0.85
        """

        # Test basic integration
        print("Basic Integration:")
        basic_integration = agent.integrated_analysis_basic(market_info, product_info, founder_info)
        print(basic_integration)
        print()

        # Test advanced integration
        print("Advanced Integration:")
        advanced_integration = agent.integrated_analysis_pro(
            market_info,
            product_info,
            founder_info,
            founder_idea_fit=0.85,
            founder_segmentation="L4",
            rf_prediction="Successful"
        )
        print(advanced_integration)

        # Test quantitative decision
        print("Quantitative Decision:")
        quant_decision = agent.getquantDecision(
            rf_prediction="Successful",
            Founder_Idea_Fit=0.85,
            Founder_Segmentation="L4"
        )
        print(quant_decision)

    # Run the test function
    test_integration_agent()
