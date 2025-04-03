from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from colorama import Fore, Style
from .prompts import AGGREGATION_SYSTEM_PROMPT


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
        raise NotImplementedError(
            "Subclasses must implement extract_pharmaceutical_data"
        )

    def aggregate_extractions(self, extractions, prompt):
        """
        Aggregate multiple extraction results.

        Args:
            extractions: List of extraction results
            prompt: The aggregation prompt

        Returns:
            Aggregated extraction in markdown format
        """
        raise NotImplementedError("Subclasses must implement aggregate_extractions")


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

    def extract_pharmaceutical_data(self, slide_image, prompt, system_prompt, tools):
        """
        Extract pharmaceutical data using a Gemini model.

        Args:
            slide_image: Base64-encoded slide image
            prompt: The user prompt for extraction
            system_prompt: The system prompt for extraction
            tools: List of tools to use for extraction

        Returns:
            Markdown-formatted extraction result
        """
        # Create ReAct agent with tools
        pharma_extractor = create_react_agent(
            model=self.model,
            tools=tools,
            prompt=system_prompt,
        )

        # Format input for Gemini models (uses image_url format with base64 data)
        extraction_input = {
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

        print(
            Fore.BLUE + f"Using {self.model_name} for extraction..." + Style.RESET_ALL
        )

        # Call the model via ReAct agent
        result = pharma_extractor.invoke(extraction_input)

        # Extract and return the markdown content
        return self._extract_markdown_content(result)

    def _extract_markdown_content(self, result):
        """
        Extract markdown content from Gemini response.
        """
        # Check for LangChain message objects first
        if hasattr(result, "content") and not callable(
            getattr(result, "content", None)
        ):
            return result.content

        # Then check if it's a specific LangChain message type
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
                    # If content contains metadata markers, extract just the text
                    if isinstance(content, str) and content.startswith("content='"):
                        # Extract the actual content between content=' and the next '
                        import re

                        match = re.match(r"content='(.+)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content
            elif "content" in result:
                return result["content"]

        # Convert to string and clean if all else fails
        result_str = str(result)
        # Try to clean up the string if it contains metadata
        if result_str.startswith("content='"):
            import re

            match = re.match(
                r"content='(.+?)' additional_kwargs=", result_str, re.DOTALL
            )
            if match:
                return match.group(1)

        return result_str

    def aggregate_extractions(self, extractions, prompt):
        """
        Aggregate multiple extraction results using a Gemini model.

        Args:
            extractions: List of extraction results
            prompt: The aggregation prompt

        Returns:
            Aggregated extraction in markdown format
        """
        print(
            Fore.BLUE + f"Using {self.model_name} for aggregation..." + Style.RESET_ALL
        )

        try:
            result = self.model.invoke(
                [
                    {"role": "system", "content": AGGREGATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]
            )
        except Exception as e:
            print(Fore.RED + f"Error in aggregation: {str(e)}" + Style.RESET_ALL)
            # If direct invocation fails, return the first extraction as a fallback
            return extractions[0] if extractions else "No extractions to aggregate"

        # Extract and return the markdown content
        return self._extract_markdown_content(result)


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

    def extract_pharmaceutical_data(self, slide_image, prompt, system_prompt, tools):
        """
        Extract pharmaceutical data using a Claude model.

        Args:
            slide_image: Base64-encoded slide image
            prompt: The user prompt for extraction
            system_prompt: The system prompt for extraction
            tools: List of tools to use for extraction

        Returns:
            Markdown-formatted extraction result
        """
        # Create ReAct agent with tools
        pharma_extractor = create_react_agent(
            model=self.model,
            tools=tools,
            prompt=system_prompt,
        )

        # Format input for Claude models (Claude uses different image format)
        # Format for Claude's multimodal API which accepts base64 directly
        extraction_input = {
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

        print(
            Fore.BLUE + f"Using {self.model_name} for extraction..." + Style.RESET_ALL
        )

        # Call the model via ReAct agent
        result = pharma_extractor.invoke(extraction_input)

        # Extract and return the markdown content
        return self._extract_markdown_content(result)

    def _extract_markdown_content(self, result):
        """
        Extract markdown content from Claude response.

        Args:
            result: Response from Claude model

        Returns:
            Extracted markdown content as string
        """
        # Check for LangChain message objects first
        if hasattr(result, "content") and not callable(
            getattr(result, "content", None)
        ):
            return result.content

        # Then check if it's a specific LangChain message type
        if "langchain_core.messages" in str(type(result)):
            if hasattr(result, "content"):
                return result.content

        # Claude typically returns content in a more structured format
        if isinstance(result, dict):
            if "messages" in result:
                # Use the last assistant message
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    content = last_message["content"]
                    # Handle content metadata format if present
                    if isinstance(content, str) and content.startswith("content='"):
                        import re

                        match = re.match(r"content='(.+?)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content
            elif "content" in result:
                return result["content"]

        # Fallback and clean if all else fails
        result_str = str(result)
        if result_str.startswith("content='"):
            import re

            match = re.match(
                r"content='(.+?)' additional_kwargs=", result_str, re.DOTALL
            )
            if match:
                return match.group(1)

        return result_str

    def aggregate_extractions(self, extractions, prompt):
        """
        Aggregate multiple extraction results using a Claude model.

        Args:
            extractions: List of extraction results
            prompt: The aggregation prompt

        Returns:
            Aggregated extraction in markdown format
        """
        print(
            Fore.BLUE + f"Using {self.model_name} for aggregation..." + Style.RESET_ALL
        )

        try:
            # Call the model directly
            result = self.model.invoke(
                [
                    {"role": "system", "content": AGGREGATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]
            )

        except Exception as e:
            print(Fore.RED + f"Error in aggregation: {str(e)}" + Style.RESET_ALL)
            # If direct invocation fails, return the first extraction as a fallback
            return extractions[0] if extractions else "No extractions to aggregate"

        # Extract and return the markdown content
        return self._extract_markdown_content(result)


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

    def extract_pharmaceutical_data(self, slide_image, prompt, system_prompt, tools):
        """
        Extract pharmaceutical data using an OpenAI model.

        Args:
            slide_image: Base64-encoded slide image
            prompt: The user prompt for extraction
            system_prompt: The system prompt for extraction
            tools: List of tools to use for extraction

        Returns:
            Markdown-formatted extraction result
        """
        # Create ReAct agent with tools
        pharma_extractor = create_react_agent(
            model=self.model,
            tools=tools,
            prompt=system_prompt,
        )

        # Format input for OpenAI models (uses content with image_url)
        extraction_input = {
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

        print(
            Fore.BLUE + f"Using {self.model_name} for extraction..." + Style.RESET_ALL
        )

        # Call the model via ReAct agent
        result = pharma_extractor.invoke(extraction_input)

        # Extract and return the markdown content
        return self._extract_markdown_content(result)

    def _extract_markdown_content(self, result):
        """
        Extract markdown content from OpenAI response.

        Args:
            result: Response from OpenAI model

        Returns:
            Extracted markdown content as string
        """
        # Check for LangChain message objects first
        if hasattr(result, "content") and not callable(
            getattr(result, "content", None)
        ):
            return result.content

        # Then check if it's a specific LangChain message type
        if "langchain_core.messages" in str(type(result)):
            if hasattr(result, "content"):
                return result.content

        # OpenAI typically returns a structured response
        if isinstance(result, dict):
            if "messages" in result:
                # Extract from messages
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    return last_message.content
                elif isinstance(last_message, dict) and "content" in last_message:
                    content = last_message["content"]
                    # Handle content metadata format if present
                    if isinstance(content, str) and content.startswith("content='"):
                        import re

                        match = re.match(r"content='(.+?)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content
            elif "choices" in result:
                # Direct API response format
                if len(result["choices"]) > 0:
                    content = result["choices"][0].get("message", {}).get("content", "")
                    if isinstance(content, str) and content.startswith("content='"):
                        import re

                        match = re.match(r"content='(.+?)'", content, re.DOTALL)
                        if match:
                            return match.group(1)
                    return content
            elif "content" in result:
                return result["content"]

        # Fallback and clean if all else fails
        result_str = str(result)
        if result_str.startswith("content='"):
            import re

            match = re.match(
                r"content='(.+?)' additional_kwargs=", result_str, re.DOTALL
            )
            if match:
                return match.group(1)

        return result_str

    def aggregate_extractions(self, extractions, prompt):
        """
        Aggregate multiple extraction results using an OpenAI model.

        Args:
            extractions: List of extraction results
            prompt: The aggregation prompt

        Returns:
            Aggregated extraction in markdown format
        """
        print(
            Fore.BLUE + f"Using {self.model_name} for aggregation..." + Style.RESET_ALL
        )

        try:
            # Call the model directly
            result = self.model.invoke(
                [
                    {"role": "system", "content": AGGREGATION_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]
            )

        except Exception as e:
            print(Fore.RED + f"Error in aggregation: {str(e)}" + Style.RESET_ALL)
            # If direct invocation fails, return the first extraction as a fallback
            return extractions[0] if extractions else "No extractions to aggregate"

        # Extract and return the markdown content
        return self._extract_markdown_content(result)


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
