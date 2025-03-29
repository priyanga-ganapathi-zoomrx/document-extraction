# tools.py
from typing import Optional, List, Dict, Any, Callable
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from .schema_data import PHARMA_SCHEMA
from .env_utils import get_env
import json
import re
import os
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
    

# Initialize vectorstore with embeddings
# Using OpenAI embeddings, but could be replaced with a local model like HuggingFace
openai_api_key = get_env("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key)
vector_store = InMemoryVectorStore(embedding=embeddings)

def parse_extraction_to_chunks(extraction_text: str, slide_number: int) -> List[Document]:
    """
    Parse an extraction markdown text into document chunks for the vector store.
    Each entity section becomes a separate chunk with appropriate metadata.
    
    Args:
        extraction_text: The markdown-formatted extraction text
        slide_number: The slide number this extraction is from
    
    Returns:
        List of Document objects ready to be added to the vector store
    """
    chunks = []
    
    # Split the extraction into sections based on entity types
    entity_pattern = r'### (.*?) \((.*?)\)(.*?)(?=### |\Z)'
    entity_matches = re.finditer(entity_pattern, extraction_text, re.DOTALL)
    
    for match in entity_matches:
        entity_type = match.group(1).strip()
        schema_table = match.group(2).strip()
        entity_content = match.group(3).strip()
        
        # Create a document for this entity
        doc = Document(
            page_content=f"Entity Type: {entity_type}\nSchema Table: {schema_table}\n{entity_content}",
            metadata={
                "entity_type": entity_type,
                "schema_table": schema_table,
                "slide_number": slide_number
            }
        )
        chunks.append(doc)
    
    # Add the full extraction as a document too
    full_doc = Document(
        page_content=extraction_text,
        metadata={
            "entity_type": "full_extraction",
            "slide_number": slide_number
        }
    )
    chunks.append(full_doc)
    
    return chunks

def update_vector_store(extraction_text: str, slide_number: int):
    """
    Update the vector store with a new extraction.
    
    Args:
        extraction_text: The markdown-formatted extraction text
        slide_number: The slide number this extraction is from
    """
    chunks = parse_extraction_to_chunks(extraction_text, slide_number)
    vector_store.add_documents(chunks)

@tool
def lookup_previous(concept: str, entity_type: Optional[str] = None, slide_range: Optional[str] = None) -> str:
    """
    Retrieve information about a concept from previously processed slides.
    
    Args:
        concept: The concept, term, or entity to search for
        entity_type: Optional entity type to narrow search (e.g., "drug", "disease")
        slide_range: Optional slide number range (e.g., "1-5")
    
    Returns:
        Relevant information from previous slides that matches the search criteria
    """
    print(Fore.CYAN + f"[TOOL - lookup_previous] Input: concept='{concept}', entity_type={entity_type}, slide_range={slide_range}" + Style.RESET_ALL)

    # Define filter function based on parameters
    def filter_func(doc: Document) -> bool:
        # Entity type filter
        if entity_type and doc.metadata.get("entity_type") != entity_type:
            return False
        
        # Slide range filter
        if slide_range:
            try:
                slide_num = doc.metadata.get("slide_number")
                if "-" in slide_range:
                    start, end = map(int, slide_range.split("-"))
                    if not (start <= slide_num <= end):
                        return False
                else:
                    if slide_num != int(slide_range):
                        return False
            except (ValueError, TypeError):
                pass  # Ignore invalid slide range formats
        
        return True
    
    try:
        # Get results from vector store with filtering
        results = vector_store.similarity_search(
            query=concept,
            k=5,  # Return top 5 most relevant results
            filter=filter_func
        )
        
        if not results:
            result_msg = f"No information found for concept '{concept}' in previous slides."
            print(Fore.CYAN + f"[TOOL - lookup_previous] Output: {result_msg}" + Style.RESET_ALL)
            return result_msg
        
        # Format the results
        formatted_results = f"### Relevant information about '{concept}' from previous slides:\n\n"
        
        for doc in results:
            slide_num = doc.metadata.get("slide_number", "Unknown")
            entity_type = doc.metadata.get("entity_type", "Unknown")
            
            # Format the content based on whether it's a full extraction or an entity
            if entity_type == "full_extraction":
                excerpt = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                formatted_results += f"**Slide {slide_num} - Full Extraction Excerpt:**\n{excerpt}\n\n"
            else:
                formatted_results += f"**Slide {slide_num} - {entity_type}:**\n{doc.page_content}\n\n"
        
        print(Fore.CYAN + f"[TOOL - lookup_previous] Output length: {len(formatted_results)} chars, found {len(results)} results" + Style.RESET_ALL)
        return formatted_results
    
    except Exception as e:
        error_msg = f"Error retrieving previous information: {str(e)}"
        print(Fore.RED + f"[TOOL - lookup_previous] Error: {error_msg}" + Style.RESET_ALL)
        return error_msg

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