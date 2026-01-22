"""
Standalone GUI Application for AI Website Testing Agent
This runs in the foreground so the browser WILL be visible
"""
from dotenv import load_dotenv
load_dotenv()

import tkinter as tk
from tkinter import scrolledtext, ttk
from threading import Thread
from agent.workflow import create_workflow
import json

class TestingAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Website Testing Agent - Real-Time Execution")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e2e')
        
        # Create workflow
        self.workflow = create_workflow()
        
        # Execution lock to prevent multiple simultaneous runs
        self.is_running = False
        
        # Header
        header = tk.Label(
            root, 
            text="🤖 AI Website Testing Agent",
            font=("Arial", 24, "bold"),
            bg='#1e1e2e',
            fg='#cdd6f4'
        )
        header.pack(pady=20)
        
        # Instruction input
        tk.Label(
            root,
            text="Enter Test Instruction:",
            font=("Arial", 12),
            bg='#1e1e2e',
            fg='#cdd6f4'
        ).pack(pady=5)
        
        self.instruction_text = scrolledtext.ScrolledText(
            root,
            height=4,
            font=("Arial", 11),
            bg='#313244',
            fg='#cdd6f4',
            insertbackground='#cdd6f4'
        )
        self.instruction_text.pack(padx=20, pady=5, fill=tk.X)
        
        # Example text
        example = "Navigate to http://127.0.0.1:5000/static/test_page.html, fill username with 'admin', fill password with 'secret', check remember me checkbox, and click login button"
        self.instruction_text.insert("1.0", example)
        
        # Run button
        self.run_button = tk.Button(
            root,
            text="▶ Run Test (Browser Will Open!)",
            font=("Arial", 14, "bold"),
            bg='#89b4fa',
            fg='#1e1e2e',
            command=self.run_test,
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        self.run_button.pack(pady=15)
        
        # Status label
        self.status_label = tk.Label(
            root,
            text="Ready to test",
            font=("Arial", 11),
            bg='#1e1e2e',
            fg='#a6e3a1'
        )
        self.status_label.pack(pady=5)
        
        # Results area
        tk.Label(
            root,
            text="Test Results:",
            font=("Arial", 12, "bold"),
            bg='#1e1e2e',
            fg='#cdd6f4'
        ).pack(pady=5)
        
        self.results_text = scrolledtext.ScrolledText(
            root,
            height=20,
            font=("Consolas", 10),
            bg='#313244',
            fg='#cdd6f4',
            state=tk.DISABLED
        )
        self.results_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
    def update_status(self, message, color='#a6e3a1'):
        self.status_label.config(text=message, fg=color)
        self.root.update()
        
    def append_result(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.root.update()
        
    def run_test(self):
        # Prevent multiple simultaneous executions
        if self.is_running:
            self.update_status("⚠️ Test already running, please wait...", '#fab387')
            return
            
        instruction = self.instruction_text.get("1.0", tk.END).strip()
        
        if not instruction:
            self.update_status("❌ Please enter a test instruction", '#f38ba8')
            return
        
        # Set running flag
        self.is_running = True
            
        # Disable button during test
        self.run_button.config(state=tk.DISABLED)
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        # Run test in thread
        thread = Thread(target=self.execute_test, args=(instruction,))
        thread.daemon = True
        thread.start()
        
    def execute_test(self, instruction):
        try:
            self.update_status("🔄 Planning test steps...", '#f9e2af')
            self.append_result("="*80)
            self.append_result(f"📝 Instruction: {instruction}")
            self.append_result("="*80)
            self.append_result("")
            
            self.update_status("🌐 Browser will open now! Watch the execution...", '#89b4fa')
            self.append_result("🌐 Executing test... (BROWSER WINDOW SHOULD BE VISIBLE)")
            self.append_result("")
            
            # Execute workflow
            result = self.workflow.invoke({"instruction": instruction})
            report = result.get("report", {})
            
            # Display results
            status = report.get("status", "UNKNOWN")
            if status == "PASS":
                self.update_status("✅ Test PASSED!", '#a6e3a1')
                status_color = "✅"
            elif status == "FAIL":
                self.update_status("❌ Test FAILED", '#f38ba8')
                status_color = "❌"
            else:
                self.update_status("⚠️ Test ERROR", '#fab387')
                status_color = "⚠️"
                
            self.append_result(f"{status_color} Status: {status}")
            self.append_result(f"📊 Total Steps: {report.get('total_steps', 0)}")
            self.append_result(f"✅ Passed: {report.get('passed', 0)}")
            self.append_result(f"❌ Failed: {report.get('failed', 0)}")
            self.append_result(f"⏱️  Execution Time: {report.get('execution_time_sec', 0)}s")
            self.append_result("")
            self.append_result("="*80)
            self.append_result("STEP DETAILS:")
            self.append_result("="*80)
            
            for step in report.get('steps', []):
                step_num = step.get('step_number', '?')
                action = step.get('action_type', 'unknown')
                success = step.get('success', False)
                status_icon = "✅" if success else "❌"
                
                self.append_result(f"\n{status_icon} Step {step_num}: {action}")
                
                if step.get('selector'):
                    self.append_result(f"   Selector: {step['selector']}")
                if step.get('value'):
                    self.append_result(f"   Value: {step['value']}")
                if step.get('execution_time_ms'):
                    self.append_result(f"   Time: {step['execution_time_ms']}ms")
                if step.get('error'):
                    self.append_result(f"   ❌ Error: {step['error']}")
                if step.get('screenshot'):
                    self.append_result(f"   📸 Screenshot: {step['screenshot']}")
                    
        except Exception as e:
            self.update_status(f"❌ Error: {str(e)}", '#f38ba8')
            self.append_result(f"\n❌ ERROR: {str(e)}")
            import traceback
            self.append_result(traceback.format_exc())
        finally:
            # Reset running flag and re-enable button
            self.is_running = False
            self.run_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestingAgentGUI(root)
    root.mainloop()
