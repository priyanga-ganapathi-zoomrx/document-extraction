from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from .prompts import *

class Agents:
    def __init__(self):
        # Initialize models
        self.claude = ChatAnthropic(model="claude-3-opus-20240229", temperature=0.1)
        
        # Create a chain that handles the message formatting and image
        def create_messages(inputs):
            # Format the text portion of the message
            formatted_text = PHARMA_EXTRACTION_USER_PROMPT_TEMPLATE.format(
                presentation_title=inputs["presentation_title"],
                company_name=inputs["company_name"],
                presentation_date=inputs["presentation_date"],
                event_name=inputs["event_name"],
                slide_number=inputs["slide_number"],
                total_slides=inputs["total_slides"],
                document_source_id=inputs["document_source_id"],
                previous_extractions=inputs["previous_extractions"]
            )
            
            # Create the messages with system prompt and human message (text + image)
            messages = [
                SystemMessage(content=PHARMA_EXTRACTION_SYSTEM_PROMPT),
                HumanMessage(content=[
                    {"type": "text", "text": formatted_text},
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": inputs["slide_image"]}}
                ])
            ]
            
            return messages
        
        # Create the extraction chain
        self.pharma_data_extractor = (
            create_messages | 
            self.claude | 
            StrOutputParser()
        )