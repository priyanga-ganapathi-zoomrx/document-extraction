# src/snippet_graph.py

import os
# import base64 # Remove base64 import
from typing import List, Dict, Any

from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from trustcall import create_extractor

# Assuming GraphState and Page are defined in src.state
from .state import GraphState, Page, ExtractedData, Snippet
from .utils import image_to_base64
from .prompt import IMAGE_TO_SNIPPET_PROMPT, SNIPPET_TO_ENRICHED_SNIPPET_PROMPT

OUTPUT_DIR = "output"
OUTPUT_FILENAME = "snippets.txt"



# --- Graph Nodes ---

def set_next_page(state: GraphState) -> GraphState:
    """Determines the next page to process or marks completion."""
    print("--- Setting Next Page ---")
    pages = state.get("pages", [])
    current_page_index = -1

    # Find the index of the current page if it exists
    current_page = state.get("current_page")
    if current_page:
        try:
            current_page_index = next(i for i, p in enumerate(pages) if p.page_number == current_page.page_number)
        except StopIteration:
            print(f"Warning: Current page {current_page.page_number} not found in pages list.")
            current_page_index = -1 # Reset if not found

    next_page_index = current_page_index + 1

    if 0 <= next_page_index < len(pages):
        next_page = pages[next_page_index]
        print(f"Next page to process: {next_page.page_number}")
        return {**state, "current_page": next_page, "processing_complete": False}
    else:
        print("No more pages to process.")
        return {**state, "current_page": None, "processing_complete": True}

def generate_page_snippet(state: GraphState) -> Dict[str, Any]:
    """Generates a text snippet for the current page image using Gemini."""
    print("--- Generating Snippet ---")
    current_page = state.get("current_page")
    pages = state.get("pages", [])

    if not current_page:
        print("No current page set. Skipping snippet generation.")
        return {"pages": pages} # Return original pages

    print(f"Processing page: {current_page.page_number}")

    # Check if snippets already exist (e.g., from a previous run)
    if current_page.snippets:
        print(f"Snippets already exist for page {current_page.page_number}. Skipping.")
        return {"pages": pages}

    # Prepare image and prompt for LLM
    base64_image = image_to_base64(current_page.image_path) # Call the imported function
    if not base64_image:
        print(f"Could not load or encode image for page {current_page.page_number}. Skipping snippet generation.")
        # Set an error snippet
        current_page.snippets = [Snippet(title="Error", content="Error loading image")]
    else:
        # Load API key from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            current_page.snippets = [Snippet(title="Error", content="Missing API Key")]
            # Decide how to handle this - skip or error out?
            # For now, we'll just set an error snippet and let the update happen
        else:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro-exp-03-25",
                google_api_key=api_key # Pass API key here
            )
            extractor = create_extractor(
                llm,
                tools=[ExtractedData],  # The top-level schema you want to populate
                tool_choice="ExtractedData" # Force the LLM to use this schema
            )
            message = HumanMessage(
                content=[
                    {"type": "text", "text": IMAGE_TO_SNIPPET_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_image}"
                    },
                ]
            )

            try:
                result = extractor.invoke([message]) 
                print(result)# Type hint for clarity

                if result and result.get("responses"):
                    extracted_data_model = result["responses"][0] # Get the Pydantic model instance
                    # Optional: Keep the JSON string if needed elsewhere, but don't use it for attribute access
                    extracted_json_string = extracted_data_model.model_dump_json(indent=2)
                    print("Extracted JSON String (for debugging):")
                    print(extracted_json_string)

                    # Directly assign the list of Snippet objects from the Pydantic model
                    current_page.snippets = extracted_data_model.snippets if extracted_data_model.snippets else []

                    # Correctly access the count from the model instance
                    print(f"Successfully extracted {len(current_page.snippets)} snippets for page {current_page.page_number}.")
                else:
                    print(f"Extraction failed or produced no snippets for page {current_page.page_number}.")
                    current_page.snippets = [Snippet(title="Warning", content="No snippets extracted.")] # Assign empty list or warning
            except Exception as e:
                print(f"Error calling LLM for page {current_page.page_number}: {e}")
                current_page.snippets = [Snippet(title="Error", content=f"Error generating snippet: {e}")]

    # --- Crucial Step: Update the page in the main list ---
    updated_pages = pages[:] # Create a shallow copy
    try:
        # Find the index and update the page object in the list
        page_index = next(i for i, p in enumerate(updated_pages) if p.page_number == current_page.page_number)
        updated_pages[page_index] = current_page
        print(f"Updated page {current_page.page_number} in state.")
    except StopIteration:
         print(f"Error: Could not find page {current_page.page_number} in state list to update snippet.")

    # Return the modified list of pages
    return {"pages": updated_pages}

def enrich_page_snippets(state: GraphState) -> Dict[str, Any]:
    current_page = state.get("current_page")
    pages = state.get("pages", [])
    if not current_page or not current_page.snippets:
        print("No current page or snippets to enrich. Skipping.")
        return {"pages": pages}

    # Initialize LLM and Tavily tool
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not set. Skipping enrichment.")
        return {"pages": pages}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-exp-03-25",
        google_api_key=api_key
    )
    tavily_tool = TavilySearch(max_results=5)
    agent = create_react_agent(llm, [tavily_tool])

    # Process each snippet
    for snippet in current_page.snippets:
        if not snippet.enriched_content:  # Only enrich if not already done
            try:
                response = agent.invoke({
                    "messages": [
                        {"role": "system", "content": SNIPPET_TO_ENRICHED_SNIPPET_PROMPT},
                        {"role": "user", "content": snippet.content}
                    ]
                })
                # Extract enriched content from the last message
                enriched_content = response["messages"][-1].content
                snippet.enriched_content = enriched_content
                print(f"Enriched snippet title: {snippet.title}")
                print(f"Enriched snippet content: {snippet.enriched_content}")
            except Exception as e:
                print(f"Error enriching snippet '{snippet.title}': {e}")
                snippet.enriched_content = f"Error: {e}"

    # Update pages list
    updated_pages = pages[:]
    try:
        page_index = next(i for i, p in enumerate(updated_pages) if p.page_number == current_page.page_number)
        updated_pages[page_index] = current_page
        print(f"Updated page {current_page.page_number} with enriched snippets.")
    except StopIteration:
        print(f"Error: Could not find page {current_page.page_number} to update.")
    return {"pages": updated_pages}

def aggregate_snippets(state: GraphState) -> Dict[str, str]:
    pages = state.get("pages", [])
    aggregated_page_texts = []
    for page in pages:
        page_header = f"## Page {page.page_number}\n"
        snippets_text = []
        if page.snippets:
            for snippet in page.snippets:
                content_text = f"### {snippet.title}\n**Original Content:**\n{snippet.content}"
                if snippet.enriched_content:
                    content_text += f"\n**Enriched Content:**\n{snippet.enriched_content}"
                snippets_text.append(content_text)
            page_content = "\n\n".join(snippets_text)
        else:
            page_content = "[Snippets not available]"
        aggregated_page_texts.append(f"{page_header}\n{page_content}")
    full_text = "\n\n---\n\n".join(aggregated_page_texts)
    return {"aggregated_snippets": full_text}

def export_snippets(state: GraphState) -> Dict:
    """Writes the aggregated snippets to a text file."""
    print("--- Exporting Snippets ---")
    aggregated_text = state.get("aggregated_snippets", "")

    if not aggregated_text:
        print("No aggregated text found to export.")
        return {}

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(aggregated_text)
        print(f"Successfully exported snippets to {output_path}")
    except Exception as e:
        print(f"Error writing snippets to file {output_path}: {e}")

    return {} # Signal completion of this node


# --- Conditional Edge Logic ---

def check_completion(state: GraphState) -> str:
    """Checks if the 'processing_complete' flag is set."""
    print("--- Checking Completion ---")
    if state.get("processing_complete", False):
        print("Processing complete.")
        return "complete"
    else:
        print("Processing not complete.")
        return "next_page"

# --- Build the Graph ---

def build_snippet_workflow():
    """Builds the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("set_next_page", set_next_page)
    workflow.add_node("generate_page_snippet", generate_page_snippet)
    workflow.add_node("aggregate_snippets", aggregate_snippets)
    workflow.add_node("enrich_page_snippets", enrich_page_snippets)
    workflow.add_node("export_snippets", export_snippets)

    # Set entry point
    workflow.set_entry_point("set_next_page")

    # Add edges
    workflow.add_edge("generate_page_snippet", "enrich_page_snippets")
    workflow.add_edge("enrich_page_snippets", "set_next_page")
    workflow.add_edge("aggregate_snippets", "export_snippets")
    workflow.add_edge("export_snippets", END)

    # Add conditional edge
    workflow.add_conditional_edges(
        "set_next_page",          # Source node
        check_completion,         # Function to determine route
        {
            "next_page": "generate_page_snippet", # If not complete, generate
            "complete": "aggregate_snippets"      # If complete, aggregate
        }
    )

    # Compile the graph
    app = workflow.compile()
    print("Snippet generation workflow compiled.")
    return app 