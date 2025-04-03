from trustcall import create_extractor
from .tools import search, lookup_previous, check_schema
from .prompts import PHARMA_EXTRACTION_SYSTEM_PROMPT, AGGREGATION_SYSTEM_PROMPT
from .state import DocumentMetadata
from .providers import create_model_provider
from colorama import Fore, Style


class Agents:
    def __init__(self, active_models=None, aggregator_model=None):
        """
        Initialize the Agents class with support for multiple model providers.

        Args:
            active_models: List of model names to use (e.g., ["gemini-1.5-pro", "claude-3-opus"])
                          If None, defaults to just gemini-1.5-pro
            aggregator_model: Model to use for aggregation
                             If None, defaults to the first model in active_models
        """
        # Initialize with default if no models specified
        self.active_models = active_models or ["gemini-1.5-pro"]
        print(
            Fore.GREEN
            + f"Initializing with models: {', '.join(self.active_models)}"
            + Style.RESET_ALL
        )

        # Define tools - same for all models
        self.tools = [search, lookup_previous, check_schema]

        # Initialize providers for each active model
        self.providers = {}
        for model_name in self.active_models:
            try:
                # Determine provider type from model name
                provider_type = self._determine_provider_type(model_name)

                # Create provider
                self.providers[model_name] = create_model_provider(
                    provider_type, model_name
                )
                print(
                    Fore.GREEN
                    + f"Successfully initialized provider for {model_name}"
                    + Style.RESET_ALL
                )

            except Exception as e:
                print(
                    Fore.RED
                    + f"Error initializing provider for {model_name}: {str(e)}"
                    + Style.RESET_ALL
                )
                # Skip this model but continue with others

        # Ensure we have at least one working provider
        if not self.providers:
            raise ValueError("No valid model providers were initialized")

        # Set default aggregator model (first available model if not specified)
        self.aggregator_model = aggregator_model or self.active_models[0]

        if self.aggregator_model not in self.providers:
            # Fallback to first available model
            self.aggregator_model = next(iter(self.providers.keys()))
            print(
                Fore.YELLOW
                + f"Specified aggregator model not available. Using {self.aggregator_model} instead."
                + Style.RESET_ALL
            )

        # Create metadata extractor using the first available model
        default_model = self.providers[self.active_models[0]].model
        self.metadata_extractor = create_extractor(
            default_model,
            tools=[DocumentMetadata, search],
            tool_choice="DocumentMetadata",
        )

    def _determine_provider_type(self, model_name):
        """
        Determine the provider type based on the model name.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Provider type string ("google", "anthropic", or "openai")
        """
        model_name = model_name.lower()

        if "gemini" in model_name:
            return "google"
        elif "claude" in model_name:
            return "anthropic"
        elif "gpt" in model_name:
            return "openai"
        else:
            # Default to Google if unclear
            print(
                Fore.YELLOW
                + f"Unknown model type for {model_name}. Assuming Google provider."
                + Style.RESET_ALL
            )
            return "google"

    def extract_with_model(self, model_name, slide_image, prompt):
        """
        Extract pharmaceutical data using the specified model.

        Args:
            model_name: Name of the model to use
            slide_image: Base64-encoded slide image
            prompt: Formatted extraction prompt

        Returns:
            Markdown-formatted extraction result
        """
        if model_name not in self.providers:
            raise ValueError(f"Model {model_name} not available")

        provider = self.providers[model_name]
        return provider.extract_pharmaceutical_data(
            slide_image, prompt, PHARMA_EXTRACTION_SYSTEM_PROMPT, self.tools
        )

    def aggregate_results(self, extractions, prompt, slide_image=None):
        """
        Aggregate multiple extraction results using ReAct methodology.

        Args:
            extractions: List of extraction results
            prompt: Formatted aggregation prompt
            slide_image: Base64-encoded slide image (optional, but enhances aggregation quality)

        Returns:
            Aggregated extraction in markdown format
        """
        if self.aggregator_model not in self.providers:
            # If aggregator model not available, fallback to the first available model
            self.aggregator_model = next(iter(self.providers.keys()))
            print(
                Fore.YELLOW
                + f"Aggregator model not available. Using {self.aggregator_model} instead."
                + Style.RESET_ALL
            )
            
        provider = self.providers[self.aggregator_model]
        
        # Check if slide image is provided
        if slide_image:
            print(
                Fore.BLUE
                + f"Aggregating with {self.aggregator_model} using ReAct agent and slide image..."
                + Style.RESET_ALL
            )
            return provider.aggregate_extractions(
                extractions, 
                prompt, 
                slide_image=slide_image,
                tools=self.tools,
                system_prompt=AGGREGATION_SYSTEM_PROMPT
            )
        else:
            print(
                Fore.YELLOW
                + f"Aggregating with {self.aggregator_model} without slide image (reduced accuracy)..."
                + Style.RESET_ALL
            )
            return provider.aggregate_extractions(
                extractions, 
                prompt,
                tools=self.tools,
                system_prompt=AGGREGATION_SYSTEM_PROMPT
            )