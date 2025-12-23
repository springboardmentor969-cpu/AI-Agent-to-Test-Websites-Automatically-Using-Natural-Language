from langgraph.graph import StateGraph

# Define state
class AgentState(dict):
    pass

# Node function
def handle_input(state: AgentState):
    user_input = state["input"]
    return {"output": f"Agent received instruction: {user_input}"}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("handler", handle_input)
graph.set_entry_point("handler")
graph.set_finish_point("handler")

app_graph = graph.compile()

# Function used by Flask
def run_agent(user_input: str) -> str:
    result = app_graph.invoke({"input": user_input})
    return result["output"]
