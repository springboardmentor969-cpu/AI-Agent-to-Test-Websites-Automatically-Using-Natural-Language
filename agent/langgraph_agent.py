from .config import config
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, List
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Instruction_parser import Instruction_Parser
from .code_generator import PlaywrightCodeGenerator
from .test_executor import TestExecutor
from .report_generator import ReportGenerator

class TestingState(TypedDict):
    """State definition for the testing workflow"""
    input: str
    parsed_test: Optional[Dict]
    generated_code: Optional[str]
    execution_result: Optional[Dict]
    report_path: Optional[str]
    error: Optional[str]
    current_step: str
    use_code_generation: bool
    config: Optional[Dict] 

class TestingAgent:
    """
    LangGraph-based agent that orchestrates the entire testing workflow.
    """
    
    def __init__(self, config: dict):
    # """Initialize the testing agent with configuration"""
     self.config = config
    
    # Initialize modules with Groq
     self.parser = Instruction_Parser(
        api_key=config['groq_api_key'],
        model=config.get('ai_model', 'llama-3.3-70b-versatile')
    )
    
     self.code_generator = PlaywrightCodeGenerator(
        api_key=config['groq_api_key'],
        model=config.get('ai_model', 'llama-3.3-70b-versatile')

    )
     
     self.executor = TestExecutor(
            headless=config.get('headless', True),
            timeout=config.get('timeout', 30000)
        )
        
     self.report_generator = ReportGenerator(
            report_dir=config.get('report_dir', 'reports')
        )
        
        # Build the workflow graph - THIS IS THE IMPORTANT PART!
     self.workflow = self._build_workflow()
    
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        workflow = StateGraph(TestingState)
        
        # Add nodes for each step
        workflow.add_node("parse_instructions", self._parse_node)
        workflow.add_node("generate_code", self._generate_code_node)
        workflow.add_node("execute_test", self._execute_node)
        workflow.add_node("generate_report", self._report_node)
        workflow.add_node("handle_error", self._error_node)
        
        # Define the workflow edges
        workflow.set_entry_point("parse_instructions")
        
        # From parsing, decide whether to generate code or execute directly
        workflow.add_conditional_edges(
            "parse_instructions",
            self._routing_logic,
            {
                "generate_code": "generate_code",
                "execute_test": "execute_test",
                "error": "handle_error"
            }
        )
        
        # From code generation to execution
        workflow.add_edge("generate_code", "execute_test")
        
        # From execution to reporting
        workflow.add_edge("execute_test", "generate_report")
        
        # From reporting to end
        workflow.add_edge("generate_report", END)
        
        # From error handling to end
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    def _routing_logic(self, state: TestingState) -> str:
        """Determine next node based on state"""
        if state.get('error'):
            return "error"
        
        if state.get('use_code_generation', False):
            return "generate_code"
        else:
            return "execute_test"
    
    def _parse_node(self, state: TestingState) -> TestingState:
        """Parse natural language instructions"""
        try:
            state['current_step'] = 'parsing'
            parsed_test = self.parser.parse(state['input'])
            state['parsed_test'] = parsed_test
            state['error'] = None
        except Exception as e:
            state['error'] = f"Parsing error: {str(e)}"
        
        return state
    
    def _generate_code_node(self, state: TestingState) -> TestingState:
        """Generate Playwright code"""
        try:
            state['current_step'] = 'code_generation'
            code = self.code_generator.generate(state['parsed_test'])
            state['generated_code'] = code
            state['error'] = None
        except Exception as e:
            state['error'] = f"Code generation error: {str(e)}"
        
        return state
    
    def _execute_node(self, state: TestingState) -> TestingState:
        """Execute the test"""
        try:
            state['current_step'] = 'execution'
            
            # Run async execution in sync context
            import asyncio
            
            if state.get('generated_code'):
                # Execute generated code
                result = asyncio.run(
                    self.executor.execute_code(
                        state['generated_code'],
                        state['parsed_test'].get('test_name', 'test')
                    )
                )
            else:
                # Execute structured test directly
                result = asyncio.run(
                    self.executor.execute_structured_test(
                        state['parsed_test']
                    )
                )
            
            state['execution_result'] = result
            state['error'] = None
        except Exception as e:
            state['error'] = f"Execution error: {str(e)}"
            state['execution_result'] = {
                'status': 'failed',
                'error': str(e),
                'test_name': state.get('parsed_test', {}).get('test_name', 'test'),
                'logs': [f"Execution failed: {str(e)}"]
            }
        
        return state
    
    def _report_node(self, state: TestingState) -> TestingState:
        """Generate test report"""
         # Initialize all paths
        report_path = None
        code_path = None

        try:
            state['current_step'] = 'reporting'
            config = state.get('config', {})
            report_format = config.get('report_format', 'html')
            
            report_path = self.report_generator.generate_report(
                state['execution_result'],
                format=report_format
            )
            state['report_path'] = report_path

            # Initialize code_path as None (IMPORTANT!)
            code_path = None
            # NEW: Save generated code if it exists
            if state.get('generated_code'):
              try: 
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                test_name = state.get('parsed_test', {}).get('test_name', 'test').replace(' ', '_')
            
                code_path = self. report_generator.save_generated_code(
                state['generated_code'],
                test_name,
                timestamp
            )
            
                if code_path:
                   state['code_path'] = code_path
                   print(f"✓ Playwright code saved to: {code_path}")
              except Exception as e:
                print(f"Warning: Could not save generated code: {e}")
                # Don't fail the whole report generation if code save fails
        
            state['error'] = None
          

        except Exception as e:
            import traceback
            print(f"Report generation error: {str(e)}")
            traceback.print_exc()
            state['error'] = f"Report generation error: {str(e)}"
        
        return state
    
    def _error_node(self, state: TestingState) -> TestingState:
        """Handle errors"""
        state['current_step'] = 'error'
        # Error already set in state
        return state
    
    async def run(self, natural_language_input: str, use_code_generation: bool = False) -> Dict:
        """
        Run the complete testing workflow.
        
        Args:
            natural_language_input: Natural language test description
            use_code_generation: Whether to generate and execute code (True) 
                                or execute steps directly (False, default)
        
        Returns:
            Final state dictionary with all results
        """
        initial_state = {
            'input': natural_language_input,
            'parsed_test': None,
            'generated_code': None,
            'execution_result': None,
            'report_path': None,
            'error': None,
            'current_step': 'initialized',
            'use_code_generation': use_code_generation,
            'config': self.config
        }
        
        # Run the workflow
        final_state = await self.workflow.ainvoke(initial_state)
        
        return final_state
    
    def run_sync(self, natural_language_input: str, use_code_generation: bool = False) -> Dict:
        """Synchronous version of run()"""
        import asyncio
        return asyncio.run(self.run(natural_language_input, use_code_generation))
    
    def get_status(self, state: Dict) -> str:
        """Get human-readable status from state"""
        if state.get('error'):
            return f"❌ Error in {state.get('current_step', 'unknown')}: {state['error']}"
        
        step = state.get('current_step', 'unknown')
        
        status_messages = {
            'initialized': '🔄 Initializing workflow...',
            'parsing': '📝 Parsing natural language instructions...',
            'code_generation': '🔧 Generating Playwright code...',
            'execution': '🚀 Executing test...',
            'reporting': '📊 Generating report...',
            'error': '❌ Error occurred'
        }
        
        return status_messages.get(step, f'Processing: {step}')
    # Test function
if __name__ == "__main__":
    test_config = {
        'groq_api_key': 'test_key',
        'ai_model': 'llama-3.3-70b-versatile',
        'headless': True,
        'timeout': 30000,
        'report_dir': 'reports',
        'report_format': 'html'
    }
    
    print("Testing TestingAgent initialization...")
    try:
        agent = TestingAgent(test_config)
        print(f"✓ Agent created successfully")
        print(f"✓ Config available: {hasattr(agent, 'config')}")
        print(f"✓ Config keys: {agent.config.keys()}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()