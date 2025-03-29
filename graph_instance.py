from src.graph import PharmDataWorkflow

# Pre-initialize the workflow for LangGraph server
workflow = PharmDataWorkflow()
app = workflow.app 