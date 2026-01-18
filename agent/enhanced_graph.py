# agent/enhanced_graph.py

from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import List, Any, Dict

from .enhanced_parser import EnhancedInstructionParser
from .enhanced_executor import EnhancedExecutor
from .reporter import Reporter

class EnhancedBatchState(BaseModel):
    """State for enhanced batch processing"""
    instructions: List[str] = []
    settings: Any = None
    parsed_sets: List[Any] = []
    exec_results: List[Any] = []
    reports: List[Any] = []
    use_ai_parsing: bool = True

def build_enhanced_batch_graph():
    """
    Build enhanced batch processing graph with AI-powered parsing
    and advanced execution capabilities
    """
    workflow = StateGraph(state_schema=EnhancedBatchState)

    parser = EnhancedInstructionParser()
    reporter = Reporter()

    def parse_batch_node(state: EnhancedBatchState):
        """Parse all instructions using enhanced parser"""
        parsed_sets = []
        for test in state.instructions:
            try:
                parsed = parser.parse(test, use_ai=state.use_ai_parsing)
                parsed_sets.append(parsed)
            except Exception as e:
                print(f"Parsing error: {e}")
                # Fallback to pattern-based parsing
                parsed = parser.parse(test, use_ai=False)
                parsed_sets.append(parsed)
        
        return {"parsed_sets": parsed_sets}

    def execute_all_node(state: EnhancedBatchState):
        """Execute all parsed action sets"""
        exec_results = []
        
        for i, actions in enumerate(state.parsed_sets):
            print(f"\n[EXECUTING TEST {i+1}/{len(state.parsed_sets)}]")
            
            # Create new executor for each test (fresh state)
            executor = EnhancedExecutor()
            
            try:
                result = executor.execute_actions(actions, settings=state.settings)
                exec_results.append(result)
            except Exception as e:
                print(f"Execution error: {e}")
                exec_results.append({
                    "success": False,
                    "logs": [f"[FATAL ERROR] {str(e)}"],
                    "screenshots": [],
                    "video": None
                })
        
        return {"exec_results": exec_results}

    def generate_reports_node(state: EnhancedBatchState):
        """Generate reports for all executions"""
        reports = []
        
        for i, result in enumerate(state.exec_results):
            simple_id = f"ID-{i+1:03}"
            
            try:
                html, js, pdf = reporter.generate_report(result, test_id=simple_id)
                reports.append({
                    "html_report": html,
                    "json_report": js,
                    "pdf_report": pdf
                })
            except Exception as e:
                print(f"Report generation error: {e}")
                reports.append({
                    "html_report": None,
                    "json_report": None,
                    "pdf_report": None,
                    "error": str(e)
                })
        
        return {"reports": reports}

    # Add nodes
    workflow.add_node("parse_batch", parse_batch_node)
    workflow.add_node("execute_all", execute_all_node)
    workflow.add_node("generate_reports", generate_reports_node)

    # Define edges
    workflow.set_entry_point("parse_batch")
    workflow.add_edge("parse_batch", "execute_all")
    workflow.add_edge("execute_all", "generate_reports")
    workflow.add_edge("generate_reports", END)

    return workflow


# Backward compatibility - keep old function name
def build_batch_graph():
    """Alias for backward compatibility"""
    return build_enhanced_batch_graph()
