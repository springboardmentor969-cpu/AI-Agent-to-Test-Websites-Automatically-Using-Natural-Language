import time
from workflow import agent_workflow

def run_agent(instruction: str, target_url: str = ""):
    start_time = time.time()

   
    state = {
        "instruction": instruction,
        "target_url": target_url or "http://localhost:5000"
    }

    try:
        final_state = agent_workflow.invoke(state)

        execution_time = round(time.time() - start_time, 2)

        return {
            "status": final_state["report"]["status"],
            "parsed_action": final_state.get("parsed_command", []),
            "full_playwright_script": final_state.get("full_playwright_script", ""),
            "execution_result": final_state.get("execution_result", {}),
            "execution_time_sec": execution_time,
            "screenshot": final_state["report"].get("screenshot")
        }

    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e),
            "execution_time_sec": round(time.time() - start_time, 2)
        }
