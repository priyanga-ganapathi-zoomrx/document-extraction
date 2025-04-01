from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from trustcall import create_extractor
from .tools import search, lookup_previous, check_schema
from .prompts import PHARMA_EXTRACTION_SYSTEM_PROMPT
from .state import DocumentMetadata
import os


class Agents:
    def __init__(self):
        """
        Initialize the Agents class.
        """
        # Initialize Gemini model with proper configuration for image processing
        self.gemini = ChatGoogleGenerativeAI(
            temperature=0, model="gemini-2.5-pro-exp-03-25"
        )

        # Define tools
        tools = [search, lookup_previous, check_schema]

        # Create the ReAct agent for pharmaceutical extraction
        self.pharma_data_extractor = create_react_agent(
            model=self.gemini,
            tools=tools,
            prompt=PHARMA_EXTRACTION_SYSTEM_PROMPT,
        )

        self.metadata_extractor = create_extractor(
            self.gemini,
            tools=[DocumentMetadata, search],
            tool_choice="DocumentMetadata",
        )
