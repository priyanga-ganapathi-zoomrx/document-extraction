from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes


class PharmDataWorkflow:
    def __init__(self, active_models=None, aggregator_model=None):
        # Initialize graph state & nodes with model configuration
        workflow = StateGraph(GraphState)
        nodes = Nodes(active_models, aggregator_model)

        # Define graph nodes - add new aggregation node
        workflow.add_node("load_document", nodes.load_document)
        workflow.add_node("extract_document_metadata", nodes.extract_document_metadata)
        workflow.add_node("process_next_slide", nodes.process_next_slide)
        workflow.add_node("extract_pharma_data", nodes.extract_pharma_data)
        workflow.add_node("aggregate_extractions", nodes.aggregate_extractions)  # New node
        workflow.add_node("check_processing_complete", nodes.check_processing_complete)
        workflow.add_node("export_results", nodes.export_results)

        # Entry point
        workflow.set_entry_point("load_document")

        # Define workflow edges - modified to include aggregation
        workflow.add_edge("load_document", "extract_document_metadata")
        workflow.add_edge("extract_document_metadata", "process_next_slide")
        workflow.add_edge("process_next_slide", "extract_pharma_data")
        workflow.add_edge("extract_pharma_data", "aggregate_extractions")  # Updated
        workflow.add_edge("aggregate_extractions", "check_processing_complete")  # Updated

        # Conditional routing for completion (unchanged)
        workflow.add_conditional_edges(
            "check_processing_complete",
            nodes.is_processing_complete,
            {"next_slide": "process_next_slide", "complete": "export_results"},
        )

        workflow.add_edge("export_results", END)

        # Compile workflow
        self.app = workflow.compile()
        
        # Store active models for later reference
        self.active_models = active_models