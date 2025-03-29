from colorama import Fore, Style
from src.graph import PharmDataWorkflow
from src.env_utils import get_env
import argparse
import os

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Extract pharmaceutical data from presentations')
    parser.add_argument('pdf_path', help='Path to the PDF file to process')
    
    args = parser.parse_args()
    
    # Ensure PDF file exists
    if not os.path.exists(args.pdf_path):
        print(Fore.RED + f"Error: PDF file not found at {args.pdf_path}" + Style.RESET_ALL)
        return
    
    # Get absolute path to the PDF file
    pdf_absolute_path = os.path.abspath(args.pdf_path)
    print(Fore.GREEN + f"Using PDF file: {pdf_absolute_path}" + Style.RESET_ALL)
    
    # Initialize workflow
    workflow = PharmDataWorkflow()
    app = workflow.app
    
    # Initial state for the workflow
    initial_state = {
        "document_metadata": None,
        "slides": [],
        "current_slide": None,
        "extracted_data": [],
        "processing_complete": False,
        "pdf_path": pdf_absolute_path,  # Add PDF path to initial state
    }
    
    # Run the extraction workflow
    print(Fore.GREEN + f"Starting workflow for {args.pdf_path}..." + Style.RESET_ALL)
    for output in app.stream(initial_state, config={"recursion_limit": 10000}):
        for key, value in output.items():
            print(Fore.CYAN + f"Finished running: {key}" + Style.RESET_ALL)
    
    print(Fore.GREEN + "Extraction complete!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()