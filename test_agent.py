from src.agent import agent

# Test the agent
instruction = "open login page, enter mahi in username, enter 1234 in password, click login"
result = agent.invoke({"instruction": instruction})

print("Agent result:")
print("Actions:", result["actions"])
print("Assertions:", result["assertions"])