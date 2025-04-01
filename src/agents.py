from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
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

        pharma_extraction_prompt_template = ChatPromptTemplate.from_messages([
            ("system", PHARMA_EXTRACTION_SYSTEM_PROMPT), # Use the detailed system prompt string
            MessagesPlaceholder(variable_name="agent_scratchpad"), # For agent's internal steps/tool calls
            ("user", "{input}"), # Represents the user query (text + image) coming from nodes.py
        ])

        pharma_agent_runnable = create_tool_calling_agent(
            llm=self.gemini,
            tools=tools,
            prompt=pharma_extraction_prompt_template, # Pass the structured prompt template
        )

        self.pharma_data_extractor = AgentExecutor(
            agent=pharma_agent_runnable,
            tools=tools,
            max_iterations=9999
        )


        self.metadata_extractor = create_extractor(
            self.gemini,
            tools=[DocumentMetadata, search],
            tool_choice="DocumentMetadata",
        )
