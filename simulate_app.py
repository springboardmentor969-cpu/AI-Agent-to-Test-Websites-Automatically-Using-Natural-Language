"""
This mimics EXACTLY what the Streamlit app does
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.graph_batch import build_batch_graph

# This is what you type in the UI
instructions_input = """Go to https://www.amazon.in/
Type "Iphone pro max" in search
Select first product
View details
Add to cart"""

print("=" * 70)
print("SIMULATING STREAMLIT APP EXECUTION")
print("=" * 70)

print("\nYour input:")
print(instructions_input)
print()

# This is what app.py does (NEW VERSION)
instructions_text = instructions_input.strip()
tests = [instructions_text]  # Single test with all steps

print(f"Number of tests: {len(tests)}")
print()

# Build the graph
graph = build_batch_graph()
app = graph.compile()

# Execute
settings = {
    "headless": True,
    "timeout": 10000
}

print("Invoking the graph...")
print("=" * 70)

result = app.invoke({
    "instructions": tests,
    "settings": settings
})

print()
print("=" * 70)
print("RESULTS:")
print("=" * 70)

exec_results = result.get("exec_results", [])
print(f"\nNumber of execution results: {len(exec_results)}")

for i, exec_res in enumerate(exec_results, 1):
    print(f"\n--- Test #{i} ---")
    success = exec_res.get("success", False)
    logs = exec_res.get("logs", [])
    
    print(f"Success: {success}")
    print(f"Number of log entries: {len(logs)}")
    print("\nLogs:")
    for log in logs:
        print(f"  {log}")

print("\n" + "=" * 70)
