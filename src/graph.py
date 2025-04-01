from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes


class PharmDataWorkflow:
    def __init__(self):
        # Initialize graph state & nodes
        workflow = StateGraph(GraphState)
        nodes = Nodes()

        # Define graph nodes
        workflow.add_node("load_document", nodes.load_document)
        workflow.add_node("extract_document_metadata", nodes.extract_document_metadata)
        workflow.add_node("process_next_slide", nodes.process_next_slide)
        workflow.add_node("extract_pharma_data", nodes.extract_pharma_data)
        workflow.add_node("check_processing_complete", nodes.check_processing_complete)
        workflow.add_node("export_results", nodes.export_results)

        # Entry point
        workflow.set_entry_point("load_document")

        # Define workflow edges
        workflow.add_edge("load_document", "extract_document_metadata")
        workflow.add_edge("extract_document_metadata", "process_next_slide")
        workflow.add_edge("process_next_slide", "extract_pharma_data")
        workflow.add_edge("extract_pharma_data", "check_processing_complete")

        # Conditional routing for completion
        workflow.add_conditional_edges(
            "check_processing_complete",
            nodes.is_processing_complete,
            {"next_slide": "process_next_slide", "complete": "export_results"},
        )

        workflow.add_edge("export_results", END)

        # Compile workflow
        self.app = workflow.compile()
