# main.py
import logging
import json
import re
from src.utils import load_vector_store
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Load Google API key from environment
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    logger.error("GOOGLE_API_KEY not found in .env file")
    raise ValueError("GOOGLE_API_KEY is required for LLM refinement")

# Define the tag-to-table mapping based on entity types and schema
tag_to_tables = {
    "drug": ["drugs"],
    "company": ["companies"],
    "disease": ["diseases"],
    "therapeutic_area": ["diseases", "therapeutic_modalities"],
    "target": ["molecular_targets"],
    "drug_class": ["drug_classes"],
    "modality": ["therapeutic_modalities"],
    "development_stage": ["drugs", "indication_specifications", "entity_milestones"],
    "geographic_region": ["geographies"],
    "clinical_milestone": ["entity_milestones", "program_terminations"],
    "timeline": [],
    "study_type": ["indication_specifications", "combination_indication_specifications"]
}

# Load schema data
try:
    with open('table_descriptions.json', 'r') as f:
        schema_data = json.load(f)
    logger.info("Schema data loaded successfully")
except Exception as e:
    logger.error(f"Failed to load table_description.json: {e}")
    raise

def extract_tags(snippet):
    """Extracts tags from an enriched snippet."""
    return set(re.findall(r'\{(\w+)\}', snippet))

def get_relevant_tables(snippet):
    """Retrieves database tables relevant to the tags in the snippet."""
    tags = extract_tags(snippet)
    matched_tables = set()
    for tag in tags:
        if tag in tag_to_tables:
            matched_tables.update(tag_to_tables[tag])
    return list(matched_tables)

def get_table_description(table_name, schema_data):
    """Fetches the description of a table from the schema data."""
    for table in schema_data['tables']:
        if table['table_name'].lower() == table_name.lower():
            return table['description']
    return None

def build_prompt(tables, snippet, schema_data):
    """Builds a prompt for the LLM to refine the table list."""
    print(tables)
    tables_with_descriptions = []
    for table in tables:
        desc = get_table_description(table, schema_data)
        if desc:
            tables_with_descriptions.append(f"Table: {table}\nDescription: {desc}")
    formatted_tables = "\n\n".join(tables_with_descriptions)

    prompt = f"""You are an AI assistant tasked with identifying relevant database tables for a given text snippet in the life sciences domain. Below is a list of candidate tables with their descriptions, followed by the snippet. Your job is to determine which of these tables are relevant to the entities and relationships mentioned in the snippet.

### Candidate Tables
{formatted_tables}

### Snippet
{snippet}

### Instructions
- Review the snippet and the table descriptions carefully.
- Select  the tables that are  relevant to the entities and relationships in the snippet.
- Consider the context and the specific information mentioned in the snippet.
- Do not include tables that are only tangentially related or not directly applicable.
- Provide your final answer as a list of table names in square brackets, e.g., [drugs, diseases].

### Response
"""
    return prompt

def refine_tables_with_llm(prompt):
    """Calls the ChatGoogleGenerativeAI model to refine the table list and extracts the result."""
    try:
        # Initialize the ChatGoogleGenerativeAI model
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro-exp-03-25",
            google_api_key=google_api_key,
            temperature=0.0  # Low temperature for deterministic output
        )
        
        # Invoke the model with the prompt
        response = llm.invoke(prompt)
        
        # Extract the text from the response (LangChain returns an AIMessage object)
        answer = response.content
        
        # Parse the table list from the response
        match = re.search(r'\[(.*?)\]', answer)
        if match:
            tables = match.group(1).split(', ')
            all_schema_tables = [t['table_name'].lower() for t in schema_data['tables']]
            return [table.strip().lower() for table in tables if table.strip().lower() in all_schema_tables]
        return []
    except Exception as e:
        logger.error(f"ChatGoogleGenerativeAI call failed: {e}")
        return []

if __name__ == "__main__":
    logger.info("Loading vector store")
    try:
        vector_store = load_vector_store()
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        vector_store = None

    # Load the snippets JSON
    try:
        with open('sources/snippets.json', 'r') as f:
            snippets_data = json.load(f)
        logger.info("Snippets data loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load snippets.json: {e}")
        raise

    # Process each page and snippet
    for page in snippets_data['pages']:
        for snippet in page['snippets']:
            # Get the enriched content
            enriched_content = snippet['enriched_content']
            
            # Step 1: Get tables from tag mapping
            tag_mapped_tables = get_relevant_tables(enriched_content)
            snippet['tag_mapped_tables'] = tag_mapped_tables
            
            # Step 2: Perform similarity search
            if vector_store is not None:
                similar_docs = vector_store.similarity_search_with_score(
                    query=enriched_content,
                    k=50
                )
                relevant_tables = [
                    (doc.metadata['table_name'], float(score))
                    for doc, score in similar_docs if score >= 0.3
                ]
            else:
                relevant_tables = []
                logger.warning("Vector store is None; skipping similarity search.")
            snippet['relevant_tables'] = relevant_tables

            # Step 3: Refine tables with LLM
            similarity_tables = [table for table, score in relevant_tables]
            all_tables = list(set(tag_mapped_tables + similarity_tables))
            prompt = build_prompt(all_tables, enriched_content, schema_data)
            refined_tables = refine_tables_with_llm(prompt)
            snippet['refined_tables'] = refined_tables

    # Save the updated data to a new JSON file
    with open('output/snippets-with-tables.json', 'w') as f:
        json.dump(snippets_data, f, indent=2)

    print("Processing complete. Output saved to 'output/snippets-with-tables.json'")