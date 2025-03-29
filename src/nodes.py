from colorama import Fore, Style
from .agents import Agents
from .pdf_tools import PDFToolsClass
from .state import GraphState, DocumentMetadata, Slide

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
                return {"processing_complete": True}
                
        print(Fore.GREEN + f"Processing slide {current_slide.slide_number} of {len(state['slides'])}..." + Style.RESET_ALL)
        return {"current_slide": current_slide}
        
    def extract_pharma_data(self, state: GraphState) -> GraphState:
        """Extract pharmaceutical data directly from slide image."""
        # Check if we have a current slide to process
        if not state.get("current_slide"):
            print(Fore.RED + "No current slide to process!" + Style.RESET_ALL)
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
        
        # Prepare input for the extraction agent
        extraction_input = {
            "presentation_title": state["document_metadata"].title,
            "company_name": state["document_metadata"].company,
            "presentation_date": state["document_metadata"].date,
            "event_name": state["document_metadata"].event,
            "slide_number": state["current_slide"].slide_number,
            "total_slides": len(state["slides"]),
            "document_source_id": state["document_metadata"].document_id,
            "previous_extractions": previous_extractions,
            "slide_image": state["current_slide"].base64_image
        }
        
        # Extract data directly from the image
        markdown_result = self.agents.pharma_data_extractor.invoke(extraction_input)
        
        # Add to extraction results
        return {"extracted_data": state["extracted_data"] + [markdown_result]}
        
    def check_processing_complete(self, state: GraphState) -> GraphState:
        return state
        
    def is_processing_complete(self, state: GraphState) -> str:
        """Check if all slides have been processed."""
        if state["processing_complete"]:
            print(Fore.GREEN + "Document processing complete!" + Style.RESET_ALL)
            return "complete"
        else:
            return "next_slide"
            
    def export_results(self, state: GraphState) -> GraphState:
        """Export extraction results."""
        print(Fore.YELLOW + "Exporting results..." + Style.RESET_ALL)
        
        # Handle case where no slides were processed
        if not state.get("extracted_data"):
            print(Fore.YELLOW + "No data was extracted. Nothing to export." + Style.RESET_ALL)
            return {}
            
        # Get export format from config
        export_format = state.get("export_format", "md")
        
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