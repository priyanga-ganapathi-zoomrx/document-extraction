from colorama import Fore, Style
from .agents import Agents
from .utils import PDFToolsClass
from .state import GraphState, DocumentMetadata
from .tools import update_vector_store
from .prompts import (
    PHARMA_EXTRACTION_USER_PROMPT_TEMPLATE,
    SLIDE_METADATA_EXTRACTION_PROMPT,
)
import os


class Nodes:
    def __init__(self):
        self.agents = Agents()
        self.pdf_tools = PDFToolsClass()

    def load_document(self, state: GraphState) -> GraphState:
        """Load PDF document and extract metadata."""
        print(Fore.YELLOW + "Loading document..." + Style.RESET_ALL)

        # Get the PDF path from the state
        pdf_path = state.get("pdf_path", "")

        slides = self.pdf_tools.process_pdf(pdf_path)

        return {
            **state,
            "slides": slides,
            "extracted_data": [],
            "processing_complete": False if slides else True,
        }

    def extract_document_metadata(self, state: GraphState) -> GraphState:
        """Extract metadata from the first slide of the document using trustcall."""
        print(
            Fore.YELLOW
            + "Extracting document metadata from first slide..."
            + Style.RESET_ALL
        )

        # Make sure we have slides to process
        if not state.get("slides"):
            print(Fore.RED + "No slides found in the document!" + Style.RESET_ALL)
            return {**state, "processing_complete": True}

        try:
            # Get the first slide
            first_slide = state["slides"][0]

            # Format the extraction input for trustcall
            extraction_input = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": SLIDE_METADATA_EXTRACTION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{first_slide.base64_image}"
                                },
                            },
                        ],
                    }
                ]
            }

            print(
                Fore.BLUE
                + "Using trustcall metadata extractor on first slide..."
                + Style.RESET_ALL
            )

            # Call the metadata extractor
            result = self.agents.metadata_extractor.invoke(extraction_input)

            # Get the structured metadata response
            document_metadata = result["responses"][0]

            # Ensure document_id is set
            document_metadata.document_id = state.get("pdf_path", "Unknown")

            print(
                Fore.GREEN
                + f"Extracted metadata: {document_metadata}"
                + Style.RESET_ALL
            )

            # Update the state with the extracted metadata
            return {**state, "document_metadata": document_metadata}

        except Exception as e:
            print(
                Fore.RED + f"Error in metadata extraction: {str(e)}" + Style.RESET_ALL
            )
            # Fallback to basic metadata
            document_metadata = DocumentMetadata(
                title=os.path.basename(state.get("pdf_path", "Unknown")),
                company="Unknown",
                date="Unknown",
                event="Unknown",
                document_id=state.get("pdf_path", "Unknown"),
            )
            return {**state, "document_metadata": document_metadata}

    def process_next_slide(self, state: GraphState) -> GraphState:
        """Get next slide for processing."""
        updated_state = state.copy()

        # Early termination checks
        if not state.get("slides"):
            print(Fore.RED + "No slides found in the document!" + Style.RESET_ALL)
            updated_state["processing_complete"] = True
            return updated_state

        if state.get("processing_complete", False):
            return updated_state

        total_slides = len(state["slides"])

        # CASE 1: First slide (no current slide yet)
        if not state.get("current_slide"):
            updated_state["current_slide"] = state["slides"][
                0
            ]  # Start with first slide
            print(
                Fore.GREEN
                + f"Processing slide 1 of {total_slides}..."
                + Style.RESET_ALL
            )
            return updated_state

        try:
            # Get current slide number
            current_slide_num = state["current_slide"].slide_number

            # Find the next slide (simple array lookup)
            # Since slide_number might not match array index (e.g., if numbering starts at 1),
            # we need to find where we are in the array
            current_position = None
            for i, slide in enumerate(state["slides"]):
                if slide.slide_number == current_slide_num:
                    current_position = i
                    break

            # Handle case where current slide wasn't found in the array
            if current_position is None:
                print(
                    Fore.RED
                    + f"Error: Current slide (number {current_slide_num}) not found in slides list"
                    + Style.RESET_ALL
                )
                updated_state["processing_complete"] = True
                return updated_state

            # Check if there's a next slide
            if current_position < total_slides - 1:
                # Move to next slide
                updated_state["current_slide"] = state["slides"][current_position + 1]
                next_slide_num = updated_state["current_slide"].slide_number
                print(
                    Fore.GREEN
                    + f"Processing slide {next_slide_num} of {total_slides}..."
                    + Style.RESET_ALL
                )
            else:
                # We've reached the end
                print(
                    Fore.GREEN
                    + "All slides have been processed. Moving to export."
                    + Style.RESET_ALL
                )
                updated_state["processing_complete"] = True

            return updated_state

        except Exception as e:
            print(
                Fore.RED + f"Error during slide navigation: {str(e)}" + Style.RESET_ALL
            )
            updated_state["processing_complete"] = (
                True  # Safety measure to avoid infinite loops
            )
            updated_state["error"] = str(e)
            return updated_state

    def extract_pharma_data(self, state: GraphState) -> GraphState:
        """Extract pharmaceutical data directly from slide image."""
        # Check if we have a current slide to process
        if not state.get("current_slide"):
            print(Fore.RED + "No current slide to process!" + Style.RESET_ALL)
            return {"processing_complete": True}

        # If processing_complete is already set, just pass it through
        if state.get("processing_complete", False):
            return {"processing_complete": True}

        print(
            Fore.YELLOW
            + "Extracting pharmaceutical data from slide image..."
            + Style.RESET_ALL
        )

        # Get previous extractions to use as context
        previous_extractions = ""
        if state["extracted_data"]:
            # Combine previous extractions but limit to avoid context window issues
            # We'll take the last 3 extractions as context
            recent_extractions = state["extracted_data"][-3:]
            for i, extraction in enumerate(recent_extractions):
                slide_num = (
                    state["current_slide"].slide_number - len(recent_extractions) + i
                )
                previous_extractions += (
                    f"### Slide {slide_num} Extraction:\n{extraction}\n\n"
                )

        formatted_text = PHARMA_EXTRACTION_USER_PROMPT_TEMPLATE.format(
            presentation_title=state["document_metadata"].title,
            company_name=state["document_metadata"].company,
            presentation_date=state["document_metadata"].date,
            event_name=state["document_metadata"].event,
            slide_number=state["current_slide"].slide_number,
            total_slides=len(state["slides"]),
            document_source_id=state["document_metadata"].document_id,
            previous_extractions=previous_extractions,
        )

        # Format for Gemini - it uses image_url format with base64 data
        print(Fore.BLUE + "Using Gemini model format for images" + Style.RESET_ALL)
        extraction_input = {
            "messages": [
                (
                    "user",
                    [
                        {"type": "text", "text": formatted_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{state['current_slide'].base64_image}"
                            },
                        },
                    ],
                )
            ]
        }

        result = self.agents.pharma_data_extractor.invoke(extraction_input)

        # Process the result from the ReAct agent
        if isinstance(result, dict) and "messages" in result:
            # The ReAct agent returns a dictionary with a "messages" key containing all messages
            # The last message is the final extraction result from the AI
            last_message = result["messages"][-1]

            # Extract the markdown content from the message
            if hasattr(last_message, "content"):
                markdown_result = last_message.content
            else:
                # Handle tuple format if that's what's returned
                markdown_result = (
                    last_message[1]
                    if isinstance(last_message, tuple)
                    else str(last_message)
                )
        else:
            # Fallback in case the result structure is different
            markdown_result = str(result)

        # Ensure markdown_result is a string
        if not isinstance(markdown_result, str):
            print(
                Fore.YELLOW
                + f"Warning: Expected string but got {type(markdown_result)}. Converting to string."
                + Style.RESET_ALL
            )
            markdown_result = str(markdown_result)

        # Add to extraction results
        updated_extractions = state["extracted_data"] + [markdown_result]

        # Update vector store with the new extraction
        update_vector_store(
            extraction_text=markdown_result,
            slide_number=state["current_slide"].slide_number,
        )

        # Add to extraction results
        return {**state, "extracted_data": updated_extractions}

    def check_processing_complete(self, state: GraphState) -> GraphState:
        """
        Check if all slides have been processed and mark state accordingly.

        This function verifies completion by comparing extraction count against slide count.

        Args:
            state: Current workflow state containing slides and extraction data

        Returns:
            Updated state with processing_complete flag set appropriately
        """
        # Make a copy to avoid modifying the original state
        updated_state = state.copy()

        # If already marked complete, nothing more to do
        if state.get("processing_complete", False):
            print(
                Fore.YELLOW + "Processing already marked as complete." + Style.RESET_ALL
            )
            return updated_state

        # Count slides and extractions
        expected_slides = len(state.get("slides", []))
        processed_slides = len(state.get("extracted_data", []))

        # Perform verification checks
        if expected_slides == 0:
            print(Fore.YELLOW + "No slides to process in document." + Style.RESET_ALL)
            updated_state["processing_complete"] = True
        elif processed_slides < expected_slides:
            # Still have slides to process
            print(
                Fore.BLUE
                + f"Progress: {processed_slides}/{expected_slides} slides processed."
                + Style.RESET_ALL
            )
            # Leave processing_complete as False
        elif processed_slides == expected_slides:
            # Perfect match - all slides processed exactly once
            print(
                Fore.GREEN
                + f"Verified all {processed_slides}/{expected_slides} slides processed."
                + Style.RESET_ALL
            )
            updated_state["processing_complete"] = True
        else:  # processed_slides > expected_slides
            # This is unusual - more extractions than slides
            print(
                Fore.YELLOW
                + f"Warning: Found {processed_slides} extractions for {expected_slides} slides."
                + Style.RESET_ALL
            )
            updated_state["processing_complete"] = True
            updated_state["extraction_warning"] = (
                "More extractions than slides detected"
            )

        return updated_state

    def is_processing_complete(self, state: GraphState) -> str:
        """Check if all slides have been processed."""
        if state.get("processing_complete", False):
            print(
                Fore.GREEN
                + "Document processing complete! Moving to export step..."
                + Style.RESET_ALL
            )
            return "complete"
        else:
            print(
                Fore.BLUE
                + "Not all slides processed yet. Moving to next slide..."
                + Style.RESET_ALL
            )
            return "next_slide"

    def export_results(self, state: GraphState) -> GraphState:
        """Export extraction results."""
        print(Fore.YELLOW + "Exporting results..." + Style.RESET_ALL)

        # Handle case where no slides were processed
        if not state.get("extracted_data"):
            print(
                Fore.YELLOW
                + "No data was extracted. Nothing to export."
                + Style.RESET_ALL
            )
            return {}

        # Create output directory if it doesn't exist
        import os

        os.makedirs("output", exist_ok=True)

        # Generate file prefix based on metadata or default
        file_prefix = "extraction"
        if state.get("document_metadata"):
            doc_id = state["document_metadata"].document_id
            file_prefix = doc_id.replace("/", "_")
        else:
            # Use timestamp if no metadata
            from datetime import datetime

            file_prefix = f"extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save combined extractions only
        with open(f"output/{file_prefix}_combined.md", "w") as f:
            for i, extraction in enumerate(state["extracted_data"]):
                slide_num = i + 1
                f.write(f"## Slide {slide_num}\n\n")
                f.write(extraction)
                f.write("\n\n---\n\n")

        print(
            Fore.GREEN
            + f"Results exported to output directory as {file_prefix}_combined.md"
            + Style.RESET_ALL
        )
        return {}
