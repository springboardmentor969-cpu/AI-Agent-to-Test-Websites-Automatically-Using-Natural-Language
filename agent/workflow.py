from agent.planner import plan_actions
from agent.playwright_executor import PlaywrightExecutor
from agent.validator import DOMValidator
from agent.report_builder import build_report
from agent.schemas import ExecutionStepResult
from agent.config import MAX_RETRIES

class SimpleWorkflow:
    """Simple workflow without LangGraph complexity"""
    
    def invoke(self, input_state: dict) -> dict:
        """Execute the testing workflow"""
        instruction = input_state.get("instruction")
        if not instruction:
            raise ValueError("instruction is required in input state")
        
        # Plan the actions
        plan = plan_actions(instruction)
        
        # Create browser instance ONCE outside retry loop
        executor = PlaywrightExecutor()
        validator = DOMValidator(executor.page)
        
        # Execute with retry logic
        attempt = 0
        results = []
        all_success = True
        
        try:
            for action in plan.actions:
                result = executor.execute(action)
                if result.success:
                    validator.validate(action)
                else:
                    all_success = False
                results.append(result)
        finally:
            executor.close()
        
        # Build report
        report = build_report(results)
        
        return {
            "instruction": instruction,
            "plan": plan,
            "results": results,
            "report": report,
            "attempt": attempt
        }

def create_workflow():
    """Create and return a workflow instance"""
    return SimpleWorkflow()
