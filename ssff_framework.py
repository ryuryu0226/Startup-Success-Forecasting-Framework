import logging
from typing import Any, Literal

from agents.market_agent import MarketAgent
from agents.product_agent import ProductAgent
from agents.founder_agent import FounderAgent
from agents.vc_scout_agent import VCScoutAgent, StartupInfo
from agents.integration_agent import IntegrationAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StartupFramework:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.market_agent = MarketAgent(model)
        self.product_agent = ProductAgent(model)
        self.founder_agent = FounderAgent(model)
        self.vc_scout_agent = VCScoutAgent(model)
        self.integration_agent = IntegrationAgent(model)

    def analyze_startup(
        self,
        startup_info_str: str,
        mode: Literal["advanced", "natural_language_advanced"] = "advanced"
    ) -> dict[str, Any]:
        # Parse the input string into a StartupInfo schema
        startup_info = self.vc_scout_agent.parse_record(startup_info_str)

        # Check if parsing was successful
        if isinstance(startup_info, dict):
            startup_info = StartupInfo(**startup_info)
        elif not isinstance(startup_info, StartupInfo):
            logger.error("Failed to parse startup info")
            return {"error": "Failed to parse startup info"}

        # Get prediction and categorization
        prediction, categorization = self.vc_scout_agent.side_evaluate(startup_info)
        logger.info(f"VCScout prediction: {prediction}")

        # Perform agent analyses
        market_analysis = self.market_agent.analyze(startup_info.model_dump(), mode)
        product_analysis = self.product_agent.analyze(startup_info.model_dump(), mode)
        founder_analysis = self.founder_agent.analyze(startup_info.model_dump(), "advanced")

        # Perform advanced founder analysis
        founder_segmentation = self.founder_agent.segment_founder(startup_info.founder_backgrounds)
        founder_idea_fit = self.founder_agent.calculate_idea_fit(startup_info.model_dump(), startup_info.founder_backgrounds)

        # Integrate analyses (pro version)
        integrated_analysis = self.integration_agent.integrated_analysis_pro(
            market_info=market_analysis.model_dump(),
            product_info=product_analysis.model_dump(),
            founder_info=founder_analysis.model_dump(),  
            founder_idea_fit=founder_idea_fit,
            founder_segmentation=founder_segmentation,
            rf_prediction=prediction,
        )

        # Integrate analyses (basic version)
        integrated_analysis_basic = self.integration_agent.integrated_analysis_basic(
            market_info=market_analysis.model_dump(),
            product_info=product_analysis.model_dump(),
            founder_info=founder_analysis.model_dump(),  
        )

        quant_decision = self.integration_agent.getquantDecision(
            prediction,
            founder_idea_fit,
            founder_segmentation,
        )

        return {
            'Final Analysis': integrated_analysis.model_dump(),
            'Market Analysis': market_analysis.model_dump(),
            'Product Analysis': product_analysis.model_dump(),
            'Founder Analysis': founder_analysis.model_dump(),
            'Founder Segmentation': founder_segmentation,
            'Founder Idea Fit': founder_idea_fit[0],
            'Categorical Prediction': prediction,
            'Categorization': categorization.model_dump(),
            'Quantitative Decision': quant_decision.model_dump(),
            'Startup Info': startup_info.model_dump(),
            'Basic Analysis': integrated_analysis_basic.model_dump(),
        }

def main():
    framework = StartupFramework("gpt-4o")
    
    # Test case: Turismocity (as an example)
    startup_info_str = """
    Turismocity is a travel search engine for Latin America that provides price comparison tools and travel deals. Eugenio Fage, the CTO and co-founder, has a background in software engineering and extensive experience in developing travel technology solutions.
    """

    print("\n=== Testing Advanced Analysis (analyze_startup) ===")
    print("-" * 80)
    
    try:
        print("\nStarting Advanced Analysis...")
        advanced_result = framework.analyze_startup(startup_info_str)
        
        print("\nADVANCED ANALYSIS RESULTS:")
        print("-" * 40)
        
        print("\n1. MARKET ANALYSIS:")
        print("-" * 20)
        print(advanced_result.get('Market Analysis', 'N/A'))
        
        print("\n2. PRODUCT ANALYSIS:")
        print("-" * 20)
        print(advanced_result.get('Product Analysis', 'N/A'))
        
        print("\n3. FOUNDER ANALYSIS:")
        print("-" * 20)
        print(advanced_result.get('Founder Analysis', 'N/A'))
        
        print("\n4. FINAL INTEGRATED ANALYSIS (PRO):")
        print("-" * 20)
        print(advanced_result.get('Final Analysis', 'N/A'))

        print("\n5. BASIC INTEGRATED ANALYSIS:")
        print("-" * 20)
        print(advanced_result.get('Basic Analysis', 'N/A'))
        
        print("\n6. QUANTITATIVE METRICS:")
        print("-" * 20)
        print(f"Founder Segmentation: {advanced_result.get('Founder Segmentation', 'N/A')}")
        print(f"Founder Idea Fit: {advanced_result.get('Founder Idea Fit', 'N/A')}")
        print(f"Categorical Prediction: {advanced_result.get('Categorical Prediction', 'N/A')}")
        print(f"Categorization: {advanced_result.get('Categorization', 'N/A')}")
        print(f"Quantitative Decision: {advanced_result.get('Quantitative Decision', 'N/A')}")
        print(f"Startup Info Parsed: {advanced_result.get('Startup Info', 'N/A')}")

    except Exception as e:
        print(f"\nError during advanced analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
