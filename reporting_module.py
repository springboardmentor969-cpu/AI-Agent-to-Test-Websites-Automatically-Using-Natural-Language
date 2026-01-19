import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class TestStatus(Enum):
    """Test execution status."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    TIMEOUT = "timeout"
    SKIPPED = "skipped"


@dataclass
class TestStep:
    """Individual test step result."""
    step_number: int
    description: str
    action_type: str
    target: Optional[str]
    status: TestStatus
    duration: float
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None


@dataclass
class TestReport:
    """Complete test execution report."""
    test_id: str
    test_name: str
    instruction: str
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime]
    duration: float
    total_steps: int
    passed_steps: int
    failed_steps: int
    steps: List[TestStep]
    assertions_passed: int
    assertions_failed: int
    error_message: Optional[str] = None
    output_log: Optional[str] = None
    error_log: Optional[str] = None
    generated_code: Optional[str] = None
    browser_info: Optional[Dict[str, Any]] = None


class ReportingModule:
    """Handles test result reporting and formatting."""
    
    def __init__(self, reports_dir: str = "test_reports"):
        self.reports_dir = os.path.join(os.path.dirname(__file__), reports_dir)
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def create_report(
        self,
        test_name: str,
        instruction: str,
        generated_code: str,
        execution_result: Dict[str, Any],
        commands: List[Dict[str, Any]],
        start_time: datetime
    ) -> TestReport:
        """
        Create a comprehensive test report from execution results.
        
        Args:
            test_name: Name of the test
            instruction: Original natural language instruction
            generated_code: Generated Playwright code
            execution_result: Execution result dictionary
            commands: List of structured commands
            start_time: Test start timestamp
            
        Returns:
            TestReport object
        """
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Determine status
        if execution_result.get("success"):
            status = TestStatus.PASSED
        elif execution_result.get("status") == "timeout":
            status = TestStatus.TIMEOUT
        elif execution_result.get("status") == "error":
            status = TestStatus.ERROR
        else:
            status = TestStatus.FAILED
        
        # Create test steps from commands
        steps = []
        for idx, cmd in enumerate(commands, 1):
            step_status = TestStatus.PASSED if status == TestStatus.PASSED else TestStatus.FAILED
            steps.append(TestStep(
                step_number=idx,
                description=cmd.get("description", ""),
                action_type=cmd.get("action_type", ""),
                target=cmd.get("target"),
                status=step_status,
                duration=0.0  # Individual step duration not tracked
            ))
        
        # Count assertions
        assertions_passed = execution_result.get("assertions_passed", 0)
        assertions_failed = execution_result.get("assertions_failed", 0)
        
        # Count steps
        passed_steps = len([s for s in steps if s.status == TestStatus.PASSED])
        failed_steps = len([s for s in steps if s.status == TestStatus.FAILED])
        
        # Generate test ID
        test_id = f"{test_name}_{start_time.strftime('%Y%m%d_%H%M%S')}"
        
        report = TestReport(
            test_id=test_id,
            test_name=test_name,
            instruction=instruction,
            status=status,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            total_steps=len(steps),
            passed_steps=passed_steps,
            failed_steps=failed_steps,
            steps=steps,
            assertions_passed=assertions_passed,
            assertions_failed=assertions_failed,
            error_message=execution_result.get("error"),
            output_log=execution_result.get("output"),
            error_log=execution_result.get("error_output"),
            generated_code=generated_code,
            browser_info={
                "headless": True,
                "browser": "chromium"
            }
        )
        
        return report
    
    def save_report(self, report: TestReport) -> str:
        """
        Save report to JSON file.
        
        Args:
            report: TestReport object
            
        Returns:
            Path to saved report file
        """
        # Convert to dictionary
        report_dict = asdict(report)
        
        # Convert datetime objects to strings
        report_dict["start_time"] = report.start_time.isoformat()
        if report.end_time:
            report_dict["end_time"] = report.end_time.isoformat()
        
        # Convert Enum to string
        report_dict["status"] = report.status.value
        for step in report_dict["steps"]:
            step["status"] = step["status"].value if isinstance(step["status"], TestStatus) else step["status"]
        
        # Save to file
        report_file = os.path.join(self.reports_dir, f"{report.test_id}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        return report_file
    
    def format_report_html(self, report: TestReport) -> str:
        """
        Format report as HTML for display.
        
        Args:
            report: TestReport object
            
        Returns:
            HTML string
        """
        status_color = {
            TestStatus.PASSED: "#4caf50",
            TestStatus.FAILED: "#f44336",
            TestStatus.ERROR: "#ff9800",
            TestStatus.TIMEOUT: "#9e9e9e"
        }
        
        status_icon = {
            TestStatus.PASSED: "✅",
            TestStatus.FAILED: "❌",
            TestStatus.ERROR: "⚠️",
            TestStatus.TIMEOUT: "⏱️"
        }
        
        color = status_color.get(report.status, "#666")
        icon = status_icon.get(report.status, "❓")
        
        html = f"""
        <div class="test-report" style="margin: 20px 0;">
            <div class="report-header" style="background: {color}; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
                <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
                    {icon} {report.test_name}
                </h2>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">{report.instruction}</p>
            </div>
            
            <div class="report-body" style="background: white; padding: 20px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 8px 8px;">
                <div class="report-summary" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div class="summary-item" style="padding: 15px; background: #f5f5f5; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: {color};">{report.status.value.upper()}</div>
                        <div style="color: #666; font-size: 14px;">Status</div>
                    </div>
                    <div class="summary-item" style="padding: 15px; background: #f5f5f5; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold;">{report.duration:.2f}s</div>
                        <div style="color: #666; font-size: 14px;">Duration</div>
                    </div>
                    <div class="summary-item" style="padding: 15px; background: #f5f5f5; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #4caf50;">{report.passed_steps}/{report.total_steps}</div>
                        <div style="color: #666; font-size: 14px;">Steps Passed</div>
                    </div>
                    <div class="summary-item" style="padding: 15px; background: #f5f5f5; border-radius: 6px;">
                        <div style="font-size: 24px; font-weight: bold; color: #4caf50;">{report.assertions_passed}</div>
                        <div style="color: #666; font-size: 14px;">Assertions Passed</div>
                    </div>
                </div>
                
                <div class="test-steps" style="margin-top: 20px;">
                    <h3 style="margin-bottom: 15px;">Test Steps</h3>
                    <div style="display: flex; flex-direction: column; gap: 10px;">
        """
        
        for step in report.steps:
            step_color = "#4caf50" if step.status == TestStatus.PASSED else "#f44336"
            step_icon = "✅" if step.status == TestStatus.PASSED else "❌"
            html += f"""
                        <div class="step-item" style="padding: 15px; border-left: 4px solid {step_color}; background: #f9f9f9; border-radius: 4px;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                                <span style="font-size: 18px;">{step_icon}</span>
                                <strong>Step {step.step_number}:</strong>
                                <span>{step.description}</span>
                            </div>
                            <div style="color: #666; font-size: 12px; margin-left: 28px;">
                                Type: {step.action_type} | Target: {step.target or 'N/A'}
                            </div>
                        </div>
            """
        
        html += """
                    </div>
                </div>
        """
        
        if report.error_message:
            html += f"""
                <div class="error-section" style="margin-top: 20px; padding: 15px; background: #ffebee; border-left: 4px solid #f44336; border-radius: 4px;">
                    <h4 style="margin-top: 0; color: #c62828;">Error Details</h4>
                    <pre style="background: white; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap;">{report.error_message}</pre>
                </div>
            """
        
        if report.output_log:
            html += f"""
                <div class="output-section" style="margin-top: 20px;">
                    <h4>Output Log</h4>
                    <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; max-height: 200px; overflow-y: auto; white-space: pre-wrap;">{report.output_log}</pre>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def format_report_json(self, report: TestReport) -> Dict[str, Any]:
        """
        Format report as JSON dictionary.
        
        Args:
            report: TestReport object
            
        Returns:
            Dictionary representation
        """
        return {
            "test_id": report.test_id,
            "test_name": report.test_name,
            "instruction": report.instruction,
            "status": report.status.value,
            "start_time": report.start_time.isoformat(),
            "end_time": report.end_time.isoformat() if report.end_time else None,
            "duration": report.duration,
            "summary": {
                "total_steps": report.total_steps,
                "passed_steps": report.passed_steps,
                "failed_steps": report.failed_steps,
                "assertions_passed": report.assertions_passed,
                "assertions_failed": report.assertions_failed
            },
            "steps": [
                {
                    "step_number": step.step_number,
                    "description": step.description,
                    "action_type": step.action_type,
                    "target": step.target,
                    "status": step.status.value
                }
                for step in report.steps
            ],
            "error_message": report.error_message,
            "browser_info": report.browser_info
        }
    
    def get_recent_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent test reports.
        
        Args:
            limit: Maximum number of reports to return
            
        Returns:
            List of report dictionaries
        """
        reports = []
        if not os.path.exists(self.reports_dir):
            return reports
        
        report_files = sorted(
            [f for f in os.listdir(self.reports_dir) if f.endswith('.json')],
            key=lambda x: os.path.getmtime(os.path.join(self.reports_dir, x)),
            reverse=True
        )[:limit]
        
        for report_file in report_files:
            file_path = os.path.join(self.reports_dir, report_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                    reports.append(report_data)
            except Exception:
                continue
        
        return reports



