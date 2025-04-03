from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from colorama import Fore, Style
from .prompts import AGGREGATION_SYSTEM_PROMPT
import re


class ModelProvider:
    """
    Base class for model providers handling extraction and aggregation.
    """

    def __init__(self, model_name):
        """
        Initialize the model provider.

        Args:
            model_name: Name of the specific model to use
        """
        self.model_name = model_name
        self.model = None  # To be initialized by subclasses

    def create_react_agent(self, tools, system_prompt):
        """
        Create a ReAct agent with the given tools and system prompt.

        Args:
            tools: List of tools to use with the agent
            system_prompt: System prompt for the agent

        Returns:
            ReAct agent
        """
        return create_react_agent(
            model=self.model,
            tools=tools,
            prompt=system_prompt,
        )

    def extract_markdown_content(self, result):
        """
        Extract markdown content from model response.
        
        Args:
            result: Result from model invocation

        Returns:
            Extracted markdown content as string
        """
        # Check for LangChain message objects first
        if hasattr(result, "content") and not callable(getattr(result, "content", None)):
            return result.content

        # Check if it's a specific LangChain message type
        if "langchain_core.messages" in str(type(result)):
            if hasattr(result, "content"):
                return result.content

        # Process the result from the ReAct agent
        if isinstance(result, dict):
            if "messages" in result:
                # The ReAct agent returns a dictionary with a "messages" key
                last_message = result["messages"][-1]

                # Extract the markdown content from the message
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    content = last_message["content"]
                    # Extract content between metadata markers if present
                    if isinstance(content, str) and content.startswith("content='"):
                        match = re.match(r"content='(.+)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content
            elif "content" in result:
                return result["content"]
            elif "choices" in result:  # OpenAI API format
                if len(result["choices"]) > 0:
                    content = result["choices"][0].get("message", {}).get("content", "")
                    if isinstance(content, str) and content.startswith("content='"):
                        match = re.match(r"content='(.+?)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content

        # Fallback to string conversion and cleaning
        result_str = str(result)
        if result_str.startswith("content='"):
            match = re.match(r"content='(.+?)' additional_kwargs=", result_str, re.DOTALL)
            if match:
                return match.group(1)

        return result_str

    def extract_pharmaceutical_data(self, slide_image, prompt, system_prompt, tools):
        """
        Extract pharmaceutical data from a slide image.

        Args:
            slide_image: Base64-encoded slide image
            prompt: The user prompt for extraction
            system_prompt: The system prompt for extraction
            tools: List of tools to use for extraction

        Returns:
            Markdown-formatted extraction result
        """
        # Create ReAct agent with tools
        pharma_extractor = self.create_react_agent(tools, system_prompt)

        # Format the extraction input with image (implemented by subclasses)
        extraction_input = self.format_extraction_input(slide_image, prompt, system_prompt)

        print(Fore.BLUE + f"Using {self.model_name} for extraction..." + Style.RESET_ALL)

        # Call the model via ReAct agent
        result = pharma_extractor.invoke(extraction_input)

        # Extract and return the markdown content
        return self.extract_markdown_content(result)

    def format_extraction_input(self, slide_image, prompt, system_prompt):
        """
        Format the extraction input for the specific model provider.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement format_extraction_input")

    def format_aggregation_input(self, slide_image, prompt, system_prompt):
        """
        Format the aggregation input for the specific model provider.
        To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement format_aggregation_input")

    def aggregate_extractions(self, extractions, prompt, slide_image=None, tools=None, system_prompt=None):
        """
        Aggregate multiple extraction results using a ReAct agent.

        Args:
            extractions: List of extraction results
            prompt: The aggregation prompt
            slide_image: Base64-encoded slide image
            tools: List of tools to use for aggregation
            system_prompt: System prompt for aggregation

        Returns:
            Aggregated extraction in markdown format
        """
        # Use AGGREGATION_SYSTEM_PROMPT as default if not provided
        if system_prompt is None:
            system_prompt = AGGREGATION_SYSTEM_PROMPT
            
        try:
            # If no tools provided, use empty list (will be updated in nodes.py)
            if tools is None:
                tools = []
                
            # Create ReAct agent with tools
            aggregator = self.create_react_agent(tools, system_prompt)

            # Format the aggregation input with image
            aggregation_input = self.format_aggregation_input(slide_image, prompt, system_prompt)

            print(Fore.BLUE + f"Using {self.model_name} for aggregation..." + Style.RESET_ALL)

            # Call the model via ReAct agent
            result = aggregator.invoke(aggregation_input)

            # Extract and return the markdown content
            return self.extract_markdown_content(result)

        except Exception as e:
            print(Fore.RED + f"Error in aggregation: {str(e)}" + Style.RESET_ALL)
            # If agent invocation fails, return the first extraction as a fallback
            return extractions[0] if extractions else "No extractions to aggregate"


class GoogleModelProvider(ModelProvider):
    """
    Provider implementation for Google (Gemini) models.
    """

    def __init__(self, model_name):
        """
        Initialize the Google model provider.

        Args:
            model_name: Name of the Gemini model to use (e.g., "gemini-1.5-pro")
        """
        super().__init__(model_name)
        print(Fore.GREEN + f"Initializing Google model: {model_name}" + Style.RESET_ALL)
        self.model = ChatGoogleGenerativeAI(temperature=0, model=model_name)

    def format_extraction_input(self, slide_image, prompt, system_prompt):
        """
        Format the extraction input for Google models.
        """
        # Format input for Gemini models (uses image_url format with base64 data)
        return {
            "messages": [
                (
                    "user",
                    [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{slide_image}"
                            },
                        },
                    ],
                )
            ]
        }

    def format_aggregation_input(self, slide_image, prompt, system_prompt):
        """
        Format the aggregation input for Google models.
        """
        # Format input for Gemini models with system message and image
        return {
            "messages": [
                (
                    "system",
                    system_prompt
                ),
                (
                    "user",
                    [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{slide_image}"
                            },
                        },
                    ],
                )
            ]
        }


class AnthropicModelProvider(ModelProvider):
    """
    Provider implementation for Anthropic (Claude) models.
    """

    def __init__(self, model_name):
        """
        Initialize the Anthropic model provider.

        Args:
            model_name: Name of the Claude model to use (e.g., "claude-3-opus-20240229")
        """
        super().__init__(model_name)
        print(
            Fore.GREEN + f"Initializing Anthropic model: {model_name}" + Style.RESET_ALL
        )
        self.model = ChatAnthropic(temperature=0, model=model_name)

    def format_extraction_input(self, slide_image, prompt, system_prompt):
        """
        Format the extraction input for Anthropic models.
        """
        # Format for Claude's multimodal API which accepts base64 directly
        return {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": slide_image,
                            },
                        },
                    ],
                }
            ]
        }

    def format_aggregation_input(self, slide_image, prompt, system_prompt):
        """
        Format the aggregation input for Anthropic models.
        """
        # Format for Claude's multimodal API with system message and image
        return {
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": slide_image,
                            },
                        },
                    ],
                }
            ]
        }


class OpenAIModelProvider(ModelProvider):
    """
    Provider implementation for OpenAI (GPT) models.
    """

    def __init__(self, model_name):
        """
        Initialize the OpenAI model provider.

        Args:
            model_name: Name of the OpenAI model to use (e.g., "gpt-4-vision-preview")
        """
        super().__init__(model_name)
        print(Fore.GREEN + f"Initializing OpenAI model: {model_name}" + Style.RESET_ALL)
        self.model = ChatOpenAI(temperature=0, model=model_name)

    def format_extraction_input(self, slide_image, prompt, system_prompt):
        """
        Format the extraction input for OpenAI models.
        """
        # Format input for OpenAI models (uses content with image_url)
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{slide_image}"
                            },
                        },
                    ],
                },
            ]
        }

    def format_aggregation_input(self, slide_image, prompt, system_prompt):
        """
        Format the aggregation input for OpenAI models.
        """
        # Format input for OpenAI models with system message and image
        return {
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{slide_image}"
                            },
                        },
                    ],
                },
            ]
        }


def create_model_provider(provider_type, model_name):
    """
    Factory function to create the appropriate model provider.

    Args:
        provider_type: Type of provider ('google', 'anthropic', 'openai')
        model_name: Name of the specific model

    Returns:
        ModelProvider instance
    """
    provider_type = provider_type.lower()

    if provider_type == "google":
        return GoogleModelProvider(model_name)
    elif provider_type == "anthropic":
        return AnthropicModelProvider(model_name)
    elif provider_type == "openai":
        return OpenAIModelProvider(model_name)
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")