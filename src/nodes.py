from colorama import Fore, Style
from .agents import Agents
from langchain_google_genai import ChatGoogleGenerativeAI
from .pdf_tools import PDFToolsClass
from .state import GraphState, DocumentMetadata, Slide
from .tools import update_vector_store
from .prompts import PHARMA_EXTRACTION_USER_PROMPT_TEMPLATE

class Nodes:
    def __init__(self):
        self.agents = Agents()
        self.pdf_tools = PDFToolsClass()
        
    def load_document(self, state: GraphState) -> GraphState:
        """Load PDF document and extract metadata."""
        print(Fore.YELLOW + "Loading document..." + Style.RESET_ALL)
        
        # Get the PDF path from the state
        pdf_path = state.get("pdf_path", "")
        
        if not pdf_path:
            print(Fore.RED + "Error: No PDF path provided in state" + Style.RESET_ALL)
            return {
                "document_metadata": None,
                "slides": [],
                "extracted_data": [],
                "processing_complete": True
            }
            
        doc_metadata, slides = self.pdf_tools.process_pdf(pdf_path)
        
        return {
            "document_metadata": doc_metadata,
            "slides": slides,
            "extracted_data": [],
            "processing_complete": False if slides else True
        }
        
    def process_next_slide(self, state: GraphState) -> GraphState:
        """Get next slide for processing."""
        if not state.get("slides"):
            print(Fore.RED + "No slides found in the document!" + Style.RESET_ALL)
            return {"processing_complete": True}
            
        # If processing_complete flag is already set, don't process any more slides
        if state.get("processing_complete", False):
            return {"processing_complete": True}
            
        if not state.get("current_slide") and state["slides"]:
            current_slide = state["slides"][0]
        else:
            # Find current slide index and get next one
            current_index = next((i for i, slide in enumerate(state["slides"]) 
                                if slide.slide_number == state["current_slide"].slide_number), -1)
            if current_index < len(state["slides"]) - 1:
                current_slide = state["slides"][current_index + 1]
            else:
                # All slides processed
                print(Fore.GREEN + "All slides have been processed. Moving to export." + Style.RESET_ALL)
                return {"processing_complete": True}
                
        print(Fore.GREEN + f"Processing slide {current_slide.slide_number} of {len(state['slides'])}..." + Style.RESET_ALL)
        return {"current_slide": current_slide}
        
    def extract_pharma_data(self, state: GraphState) -> GraphState:
        """Extract pharmaceutical data directly from slide image."""
        # Check if we have a current slide to process
        if not state.get("current_slide"):
            print(Fore.RED + "No current slide to process!" + Style.RESET_ALL)
            return {"processing_complete": True}
            
        # If processing_complete is already set, just pass it through
        if state.get("processing_complete", False):
            return {"processing_complete": True}
            
        print(Fore.YELLOW + "Extracting pharmaceutical data from slide image..." + Style.RESET_ALL)
        
        # Get previous extractions to use as context
        previous_extractions = ""
        if state["extracted_data"]:
            # Combine previous extractions but limit to avoid context window issues
            # We'll take the last 3 extractions as context
            recent_extractions = state["extracted_data"][-3:]
            for i, extraction in enumerate(recent_extractions):
                slide_num = state["current_slide"].slide_number - len(recent_extractions) + i
                previous_extractions += f"### Slide {slide_num} Extraction:\n{extraction}\n\n"
        
        formatted_text = PHARMA_EXTRACTION_USER_PROMPT_TEMPLATE.format(
            presentation_title=state["document_metadata"].title,
            company_name=state["document_metadata"].company,
            presentation_date=state["document_metadata"].date,
            event_name=state["document_metadata"].event,
            slide_number=state["current_slide"].slide_number,
            total_slides=len(state["slides"]),
            document_source_id=state["document_metadata"].document_id,
            previous_extractions=previous_extractions
        )
        
        # Format for Gemini - it uses image_url format with base64 data
        print(Fore.BLUE + "Using Gemini model format for images" + Style.RESET_ALL)
        extraction_input = {
            "messages": [
                ("user", [
                    {"type": "text", "text": formatted_text},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{state['current_slide'].base64_image}"
                    }}
                ])
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
                markdown_result = last_message[1] if isinstance(last_message, tuple) else str(last_message)
        else:
            # Fallback in case the result structure is different
            markdown_result = str(result)

        # Add to extraction results
        updated_extractions = state["extracted_data"] + [markdown_result]

        # Update vector store with the new extraction
        update_vector_store(
            extraction_text=markdown_result,
            slide_number=state["current_slide"].slide_number
        )
        
        # Add to extraction results
        return {"extracted_data": updated_extractions}
        
    def check_processing_complete(self, state: GraphState) -> GraphState:
        """Check if processing is complete and prepare for the next step."""
        # This is a good place to add any cleanup or final processing before checking completion
        
        # If the processing_complete flag is already set, just return the state
        if state.get("processing_complete", False):
            print(Fore.YELLOW + "Processing already marked as complete." + Style.RESET_ALL)
        
        # You could add additional logic here if needed
        # For example, checking if we've processed the expected number of slides
        expected_slides = len(state.get("slides", []))
        processed_slides = len(state.get("extracted_data", []))
        
        if expected_slides > 0 and processed_slides >= expected_slides:
            print(Fore.GREEN + f"Verified all {processed_slides}/{expected_slides} slides processed." + Style.RESET_ALL)
            return {"processing_complete": True, **state}
            
        return state
        
    def is_processing_complete(self, state: GraphState) -> str:
        """Check if all slides have been processed."""
        if state.get("processing_complete", False):
            print(Fore.GREEN + "Document processing complete! Moving to export step..." + Style.RESET_ALL)
            return "complete"
        else:
            print(Fore.BLUE + "Not all slides processed yet. Moving to next slide..." + Style.RESET_ALL)
            return "next_slide"
            
    def export_results(self, state: GraphState) -> GraphState:
        """Export extraction results."""
        print(Fore.YELLOW + "Exporting results..." + Style.RESET_ALL)
        
        # Handle case where no slides were processed
        if not state.get("extracted_data"):
            print(Fore.YELLOW + "No data was extracted. Nothing to export." + Style.RESET_ALL)
            return {}
            
        
        # Create output directory if it doesn't exist
        import os
        os.makedirs("output", exist_ok=True)
        
        # Generate file prefix based on metadata or default
        file_prefix = "extraction"
        if state.get("document_metadata"):
            doc_id = state["document_metadata"].document_id
            file_prefix = doc_id.replace('/', '_')
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
        
        print(Fore.GREEN + f"Results exported to output directory as {file_prefix}_combined.md" + Style.RESET_ALL)
        return {}