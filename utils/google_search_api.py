import os
import logging
import serpapi
from dotenv import load_dotenv

# Configure basic logging if not already configured by the main script
# This is a failsafe; ideally, the main script configures logging.
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s')

# Load environment variables from .env file in the project root
# Assumes .env is in the parent directory of 'utils'
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    logging.info(f"Loaded .env file from: {dotenv_path}")
else:
    logging.info(".env file not found at project root, relying on system environment variables or other secrets management.")

class GoogleSearchAPI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        serpapi_key = None
        key_source = "Unknown"

        # 1. Try os.getenv()
        serpapi_key = os.getenv("SERPAPI_API_KEY")
        if serpapi_key:
            key_source = "os.getenv (potentially from .env)"
        
        # 2. Fallback to Streamlit secrets if not found and Streamlit is available
        if not serpapi_key:
            try:
                import streamlit as st
                serpapi_key = st.secrets.get("SERPAPI_API_KEY")
                if serpapi_key:
                    key_source = "Streamlit secrets"
            except ImportError:
                self.logger.debug("Streamlit is not installed or not in a Streamlit environment, skipping Streamlit secrets for SERPAPI_API_KEY.")
            except Exception as e: # Broad exception for other st.secrets issues
                self.logger.debug(f"Error trying to access Streamlit secrets for SERPAPI_API_KEY: {e}")

        self.logger.info(f"Attempting to use SerpAPI Key from {key_source}. Key: {'**********' + serpapi_key[-4:] if serpapi_key else 'Not Found'}")

        if not serpapi_key:
            self.logger.error("SERPAPI_API_KEY not found through os.getenv, .env, or Streamlit secrets.")
            raise ValueError("SERPAPI_API_KEY not found.")
        self.api_key = serpapi_key

    def search(self, query, num_results=5):
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        search = serpapi.search(params)
        results = search.as_dict()
        return results.get('organic_results', [])

if __name__ == "__main__":
    
    # Setup basic logging for the __main__ block, if not already set
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO)

    print("Testing Google Search API...")

    # Test GoogleSearchAPI
    google_api = GoogleSearchAPI()
    search_results = google_api.search("Python programming")
    print("Google Search API Test:")
    for i, result in enumerate(search_results[:3], 1):  # Print first 3 results
        print(f"{i}. {result['title']}")
        print(f"   {result['link']}")
        print()
