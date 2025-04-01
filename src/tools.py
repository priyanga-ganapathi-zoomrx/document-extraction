# tools.py
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_core.documents import Document
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_openai import OpenAIEmbeddings
from .constants import PHARMA_SCHEMA
from .env_utils import get_env
import json
from colorama import Fore, Style

# Initialize the underlying Tavily search API with explicit API key
tavily_api_key = get_env("TAVILY_API_KEY", required=True)

tavily_api = TavilySearch(
    max_results=5,
    topic="general", 
    include_domains=["pubmed.ncbi.nlm.nih.gov", "clinicaltrials.gov", "fda.gov"],
    search_depth="advanced",
    tavily_api_key=tavily_api_key
)

@tool
def search(term: str) -> str:
    """
    
    Look up unknown drugs, companies, or technical terms using the Tavily search API.
    
    Args:
        term: The pharmaceutical term, drug name, company, or concept to search for.
              Be specific and include context when possible.
    
    Returns:
        Relevant information about the searched term from trusted sources.
    """
    print(Fore.CYAN + f"[TOOL - search] Input: {term}" + Style.RESET_ALL)
    try:
        # Call the Tavily API with the search term
        search_results = tavily_api.invoke({"query": f"pharmaceutical {term}"})
        
        # Format results for readability in the agent's context
        formatted_results = "### Search Results\n\n"
        
        if isinstance(search_results, dict) and "results" in search_results:
            # Handle direct API response format
            results = search_results["results"]
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. **{result['title']}**\n"
                formatted_results += f"   {result['content']}\n\n"
        else:
            # Handle string response format (when used with a ToolMessage)
            formatted_results += search_results
        
        print(Fore.CYAN + f"[TOOL - search] Output length: {len(formatted_results)} chars" + Style.RESET_ALL)
        return formatted_results
    except Exception as e:
        error_msg = f"Error performing search: {str(e)}"
        print(Fore.RED + f"[TOOL - search] Error: {error_msg}" + Style.RESET_ALL)
        return error_msg
    
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = DocArrayInMemorySearch.from_documents(
    documents=[],
    embedding=embeddings
)

def update_vector_store(extraction_text: str, slide_number: int):
    """Add an extraction to the vector store."""
    try:
        # Add the extraction as a document with slide number as metadata
        doc = Document(
            page_content=extraction_text,
            metadata={"slide_number": slide_number}
        )
        
        # Add to vector store
        vector_store.add_documents([doc])
        print(Fore.GREEN + f"Added extraction from slide {slide_number} to vector store" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error updating vector store: {str(e)}" + Style.RESET_ALL)

@tool
def lookup_previous(concept: str) -> str:
    """
    Retrieve information about a concept from previously processed slides.
    
    Args:
        concept: The concept, term, or entity to search for (e.g., drug name, disease, company)
    
    Returns:
        Relevant information from previous slides that matches the search concept
    """
    try:
        # Perform similarity search
        results = vector_store.similarity_search(
            query=concept,
            k=3  # Return top 3 most relevant results
        )
        
        if not results:
            return f"No information found about '{concept}' in previous slides."
        
        # Format results - return full slide content
        formatted_results = f"### Information about '{concept}' from previous slides:\n\n"
        
        for doc in results:
            slide_num = doc.metadata.get("slide_number", "Unknown")
            
            # Include the full slide content
            formatted_results += f"**From Slide {slide_num}:**\n\n{doc.page_content}\n\n---\n\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching previous slides: {str(e)}"

@tool
def check_schema(entity_type: str) -> str:
    """
    Verify schema requirements for a specific entity type or table.
    
    Args:
        entity_type: The entity type or table name to look up (e.g., "drug", "clinical_trials", "regulatory")
        
    Returns:
        JSON-formatted schema information about the requested entity type
    """
    print(Fore.CYAN + f"[TOOL - check_schema] Input: entity_type='{entity_type}'" + Style.RESET_ALL)
    # Normalize the entity type to handle common variations
    entity_type = entity_type.strip().lower()
    
    # Handle common singular/plural variations
    if entity_type == "drug":
        entity_type = "drugs"
    elif entity_type == "company":
        entity_type = "companies"
    elif entity_type == "disease":
        entity_type = "diseases"
    elif entity_type == "target":
        entity_type = "molecular_targets"
    
    # First, search for the entity as a table name directly in any module
    for module_name, module_tables in PHARMA_SCHEMA.items():
        if entity_type in module_tables:
            result = {
                "module": module_name,
                "table": entity_type,
                "description": module_tables[entity_type]["description"],
                "fields": module_tables[entity_type]["fields"]
            }
            json_result = json.dumps(result, indent=2)
            print(Fore.CYAN + f"[TOOL - check_schema] Output: Found exact table match for '{entity_type}'" + Style.RESET_ALL)
            return json_result
    
    # If not found as a table, check if it's a module name
    if entity_type in PHARMA_SCHEMA:
        result = {
            "module": entity_type,
            "tables": {}
        }
        for table_name, table_data in PHARMA_SCHEMA[entity_type].items():
            result["tables"][table_name] = {
                "description": table_data["description"],
                "field_count": len(table_data["fields"])
            }
        json_result = json.dumps(result, indent=2)
        print(Fore.CYAN + f"[TOOL - check_schema] Output: Found module match for '{entity_type}' with {len(result['tables'])} tables" + Style.RESET_ALL)
        return json_result
    
    # If we still haven't found it, look for partial matches
    matches = []
    
    # Check for partial table name matches
    for module_name, module_tables in PHARMA_SCHEMA.items():
        for table_name in module_tables:
            if entity_type in table_name:
                matches.append({
                    "module": module_name,
                    "table": table_name,
                    "description": module_tables[table_name]["description"]
                })
    
    if matches:
        result = {
            "partial_matches": matches
        }
        json_result = json.dumps(result, indent=2)
        print(Fore.CYAN + f"[TOOL - check_schema] Output: Found {len(matches)} partial matches for '{entity_type}'" + Style.RESET_ALL)
        return json_result
    
    # If no matches found, return a helpful error
    error_result = json.dumps({
        "error": f"No schema information found for '{entity_type}'",
        "suggestion": "Try a common entity like 'drugs', 'companies', 'diseases', or a module name like 'clinical', 'regulatory'"
    }, indent=2)
    print(Fore.RED + f"[TOOL - check_schema] Output: No matches found for '{entity_type}'" + Style.RESET_ALL)
    return error_result