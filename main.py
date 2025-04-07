from src.utils import convert_pdf_to_images
from src.state import GraphState
from src.snippet_graph import build_snippet_workflow
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example usage
if __name__ == "__main__":
    input_pdf = "./sources/novartis-jpm25.pdf"  # Replace with your PDF path

    pages = convert_pdf_to_images(input_pdf)

    # Initialize GraphState
    initial_state = GraphState(
        pages=pages,
        current_page=None,
        processing_complete=False,
        aggregated_snippets=""
    )


    snippet_workflow = build_snippet_workflow()
    
    for output in snippet_workflow.stream(initial_state, config={"recursion_limit": 10000}):
        for key, value in output.items():
            print(f"Finished running node: {key}")
            pass
