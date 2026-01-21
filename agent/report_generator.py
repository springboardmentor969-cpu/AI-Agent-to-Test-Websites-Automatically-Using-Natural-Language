from datetime import datetime
from pydoc import html
from typing import Dict
import json
import os
from unittest import result

class ReportGenerator:
    """
    Generates formatted test reports in various formats (HTML, JSON).
    """
    
    def __init__(self, report_dir: str = 'reports'):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, test_result: Dict, format: str = 'html') -> str:
        """
        Generate test report in specified format.
        
        Args:
            test_result: Test execution results dictionary
            format: Report format ('html', 'json', or 'both')
            
        Returns:
            Path to generated report file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_name = test_result.get('test_name', 'test').replace(' ', '_')
        
        if format == 'json' or format == 'both':
            json_path = self._generate_json(test_result, test_name, timestamp)
        
        if format == 'html' or format == 'both':
            html_path = self._generate_html(test_result, test_name, timestamp)
            return html_path
        
        return json_path if format == 'json' else html_path
    
    def _generate_json(self, test_result: Dict, test_name: str, timestamp: str) -> str:
        """Generate JSON report"""
        filename = f"{test_name}_{timestamp}.json"
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(test_result, f, indent=2)
        
        return filepath
    
    def _generate_html(self, test_result: Dict, test_name: str, timestamp: str) -> str:
        """Generate HTML report"""
        filename = f"{test_name}_{timestamp}.html"
        filepath = os.path.join(self.report_dir, filename)
        
        html_content = self._create_html_report(test_result)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _create_html_report(self, result: Dict) -> str:
        """Create HTML report content"""
    
        #  # DEBUG: Print what we received
        # print("=== REPORT GENERATOR DEBUG ===")
        # print(f"Result keys: {result.keys()}")
        # print(f"Has logs key: {'logs' in result}")
        # print(f"Logs value: {result.get('logs', 'KEY NOT FOUND')}")
        # print("=============================")
        if 'logs' not in result:
           result['logs'] = ['No execution logs available']

        def _create_html_report(self, result: Dict) -> str:
         """Create HTML report content"""
    
         # EMERGENCY FIX: Ensure ALL required keys exist with defaults
        defaults = {
        'status': 'unknown',
        'test_name': 'Test Report',
        'duration': 0,
        'passed_steps': 0,
        'failed_steps': 0,
        'total_steps': 0,
        'logs': [],
        'screenshots': [],
        'step_results': [],
        'error': None,
        'traceback': None
    }
    
        # Add any missing keys
        for key, default_value in defaults.items():
           if key not in result:
            result[key] = default_value
    
          # Now proceed with report generation
           status = str(result['status'])
           test_name = str(result['test_name'])
           # ... rest of your code   

        status = str(result.get('status', 'unknown'))
        test_name = str(result.get('test_name', 'Test Report'))
        duration = float(result.get('duration', 0))
        passed_steps = int(result.get('passed_steps', 0))
        failed_steps = int(result.get('failed_steps', 0))
        total_steps = int(result.get('total_steps', 0))

        status_color = {
        'passed': '#10b981',
        'failed': '#ef4444',
        'running': '#f59e0b'
         }.get(status, '#6b7280')
    
        # Use simple text instead of Unicode symbols
        status_icon = {
        'passed': 'PASS',
        'failed': 'FAIL',
        'running': 'RUNNING'
         }.get(status, 'UNKNOWN')
    
        # Generate step results HTML
        step_results_html = ''
        step_results = result.get('step_results', []) 
        if 'step_results' in result:
          for step in result['step_results']:
            step_status = step.get('status', 'unknown')
            step_icon = 'PASS' if step_status == 'passed' else 'FAIL'
            step_color = '#10b981' if step_status == 'passed' else '#ef4444'
            
            error_html = ''
            if step.get('error'):
                error_html = f"""
                <div style="margin-left: 30px; padding: 10px; background: #fee; border-left: 3px solid #ef4444; margin-top: 5px;">
                    <strong>Error:</strong> {step['error']}
                </div>
                """
            
            step_results_html += f"""
            <div style="padding: 12px; border-left: 3px solid {step_color}; margin-bottom: 10px; background: #f9fafb;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-weight: bold; color: {step_color};">[{step_icon}]</span>
                    <div>
                        <div style="font-weight: 600;">Step {step['step_number']}: {step['action'].upper()}</div>
                        <div style="color: #6b7280; margin-top: 3px;">{step['description']}</div>
                        <div style="color: #9ca3af; font-size: 12px; margin-top: 3px;">
                            Duration: {step.get('duration', 0):.2f}s
                        </div>
                    </div>
                </div>
                {error_html}
            </div>
            """
    
       # Generate logs HTML
        logs_html = ''
        logs = result.get('logs', [])  # Use .get() with default []
        if logs:
         logs_html = '<div style="background: #1f2937; color: #e5e7eb; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 13px; max-height: 300px; overflow-y: auto;">'
        for log in result['logs']:
            logs_html += f'<div style="margin-bottom: 5px;">{log}</div>'
        logs_html += '</div>'
    
        # Generate screenshots HTML
        screenshots_html = ''
        screenshots = result.get('screenshots', [])  # Use .get() with default []

        if screenshots:
         screenshots_html = '<div style="margin-top: 20px;"><h3>Screenshots</h3>'
        for screenshot in result['screenshots']:
            screenshots_html += f'<img src="/{screenshot}" style="max-width: 100%; border: 1px solid #e5e7eb; margin: 10px 0;" />'
        screenshots_html += '</div>'
    
         # Error traceback
        traceback_html = ''
        if result.get('traceback'):
         traceback_html = f"""
        <div style="margin-top: 20px;">
            <h3>Error Traceback</h3>
            <pre style="background: #1f2937; color: #ef4444; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 12px;">{result['traceback']}</pre>
        </div>
        """
    
        html = f"""<!DOCTYPE html>
       <html lang="en">
      <head>
      <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - {result.get('test_name', 'Test')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; background: #f3f4f6; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); overflow: hidden; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .status-badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; background: {status_color}; color: white; font-weight: 600; font-size: 14px; }}
        .content {{ padding: 30px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ padding: 20px; background: #f9fafb; border-radius: 8px; border-left: 4px solid #667eea; }}
        .metric-label {{ color: #6b7280; font-size: 14px; margin-bottom: 5px; }}
        .metric-value {{ font-size: 24px; font-weight: 700; color: #1f2937; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{ font-size: 20px; margin-bottom: 15px; color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }}
        h3 {{ font-size: 16px; margin: 20px 0 10px 0; color: #374151; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{result.get('test_name', 'Test Report')}</h1>
            <div style="margin-top: 10px;">
                <span class="status-badge">[{status_icon}]</span>
            </div>
            <div style="margin-top: 15px; opacity: 0.9; font-size: 14px;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        <div class="content">
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Duration</div>
                    <div class="metric-value">{result.get('duration', 0):.2f}s</div>
                </div>
                <div class="metric-card" style="border-left-color: #10b981;">
                    <div class="metric-label">Passed Steps</div>
                    <div class="metric-value" style="color: #10b981;">{result.get('passed_steps', 0)}</div>
                </div>
                <div class="metric-card" style="border-left-color: #ef4444;">
                    <div class="metric-label">Failed Steps</div>
                    <div class="metric-value" style="color: #ef4444;">{result.get('failed_steps', 0)}</div>
                </div>
                <div class="metric-card" style="border-left-color: #6b7280;">
                    <div class="metric-label">Total Steps</div>
                    <div class="metric-value">{result.get('total_steps', 0)}</div>
                </div>
            </div>
            <div class="section">
                <h2>Test Steps</h2>
                {step_results_html if step_results_html else '<p style="color: #6b7280;">No step details available</p>'}
            </div>
            {f'<div class="section"><h2>Execution Logs</h2>{logs_html}</div>' if logs_html else ''}
            {traceback_html}
            {screenshots_html}
        </div>
    </div>
</body>
</html>"""
        return html  # This MUST be indented at the same level as the 'html =' line above

    def save_generated_code(self, code: str, test_name: str, timestamp: str) -> str:
     """Save generated Playwright code to a file"""
     filename = f"{test_name}_code_{timestamp}.py"
     filepath = os.path.join(self.report_dir, filename)
     try:
       with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
            print(f"Generated code saved to: {filepath}")
            return filepath
     except Exception as e:
        print(f"Error saving code: {e}")
        return None

    def generate_summary(self, result: Dict) -> str:
        """Generate a text summary of the test results"""
        status = result.get('status', 'unknown').upper()
        test_name = result.get('test_name', 'Unnamed Test')
        duration = result.get('duration', 0)
        passed = result.get('passed_steps', 0)
        failed = result.get('failed_steps', 0)
        total = result.get('total_steps', 0)
        
        summary = f"""



Test Name: {test_name}
Status: {status}
Duration: {duration:.2f} seconds

Steps Summary:
   Passed: {passed}/{total}
   Failed: {failed}/{total}

"""
        
        if result.get('error'):
            summary += f"\nError: {result['error']}\n"
        
        return summary