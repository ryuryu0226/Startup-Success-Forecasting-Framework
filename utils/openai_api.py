import os
import logging
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
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

class OpenAIAPI:
    def __init__(self, model_name):
        """
        Initialize the OpenAIAPI with the given model name.
        """
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        api_key = None

        # 1. Try os.getenv() first (which load_dotenv() should populate if .env exists)
        api_key = os.getenv("OPENAI_API_KEY")
        # 2. Fallback to Streamlit secrets if not found via os.getenv() AND if Streamlit is available
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("OPENAI_API_KEY")
            except ImportError:
                self.logger.debug("Streamlit is not installed or not in a Streamlit environment, skipping Streamlit secrets.")
            except Exception as e:
                self.logger.debug(f"Error trying to access Streamlit secrets: {e}")

        if not api_key:
            self.logger.error("OPENAI_API_KEY not found through os.getenv, .env, or Streamlit secrets.")
            raise ValueError("OPENAI_API_KEY not found.")
        
        self.client = OpenAI(api_key=api_key)

    def get_completion(self, system_content: str, user_content: str) -> Optional[str]:
        """
        Get a completion from the OpenAI API.
        """
        self.logger.debug(f"Requesting completion. Model: {self.model_name}, System: '{system_content[:50]}...', User: '{user_content[:50]}...'")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ]
            )
            response_content = completion.choices[0].message.content
            self.logger.debug(f"Completion received: '{response_content[:100]}...'")
            return response_content
        except Exception as e:
            self.logger.error(f"An error occurred during get_completion: {e}", exc_info=True)
            return None

    def get_structured_output(
        self,
        schema_class: BaseModel,
        user_prompt: str,
        system_prompt: str,
    ) -> Optional[BaseModel]:
        """
        Structure the output according to the provided schema, user prompt, and system prompt.
        """
        self.logger.debug(f"Requesting structured output. Model: {self.model_name}, Schema: {schema_class.__name__}, System: '{system_prompt[:50]}...', User: '{user_prompt[:50]}...'")
        try:
            self.logger.debug("Calling OpenAI client.beta.chat.completions.parse...")
            completion = self.client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=schema_class,
            )
            self.logger.debug(f"Raw completion object from parse: {completion}")

            if completion and completion.choices and len(completion.choices) > 0:
                if hasattr(completion.choices[0], 'message') and completion.choices[0].message:
                    if hasattr(completion.choices[0].message, 'parsed'):
                        response = completion.choices[0].message.parsed
                        self.logger.debug(f"Parsed response: {response}")
                        return response
                    else:
                        self.logger.error("Completion choice message does not have 'parsed' attribute.")
                        self.logger.error(f"Message object: {completion.choices[0].message}")
                        return None
                else:
                    self.logger.error("Completion choice does not have 'message' attribute or message is None.")
                    self.logger.error(f"Choice object: {completion.choices[0]}")
                    return None
            else:
                self.logger.error("Completion object is None, has no choices, or choices list is empty.")
                return None
        except Exception as e:
            self.logger.error(f"An error occurred during get_structured_output: {e}", exc_info=True)
            return None

    def get_embeddings(self, text: str) -> Optional[list[float]]:
        """
        Get embeddings for the given text.
        """
        self.logger.debug(f"Requesting embeddings for text: '{text[:50]}...'")
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-large",  # You might want to make this configurable
                dimensions = 100,
            )
            self.logger.debug(f"Embedding response: {response}")
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"An error occurred while getting embeddings: {e}", exc_info=True)
            return None

if __name__ == "__main__":
    
    # Setup basic logging for the __main__ block, if not already set
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO)

    print("Testing OpenAI API...")

    # Test OpenAIAPI
    openai_api = OpenAIAPI("gpt-4o")  # Use an appropriate model name
    
    # Test get_completion
    system_content = "You are a helpful assistant."
    user_content = "What's the capital of France?"
    completion = openai_api.get_completion(system_content, user_content)
    print("OpenAI Completion Test:")
    print(completion)
    print()

    # Test get_structured_output
    from pydantic import BaseModel, Field

    class WeatherResponse(BaseModel):
        temperature: float = Field(..., description="Temperature in Celsius")
        conditions: str = Field(..., description="Weather conditions (e.g., sunny, rainy)")

    system_prompt = "You are a weather reporting system. Provide weather information based on the user's query."
    user_prompt = "What's the weather like in Paris today?"
    structured_output = openai_api.get_structured_output(WeatherResponse, user_prompt, system_prompt)
    print("OpenAI Structured Output Test:")
    print(structured_output)
    print()

    # Test get_embeddings
    text = "This is a test sentence for embeddings."
    embeddings = openai_api.get_embeddings(text)
    print("OpenAI Embeddings Test:")
    print(f"Embedding vector length: {len(embeddings)}")
    print(f"First 5 values: {embeddings[:5]}")
    print()
