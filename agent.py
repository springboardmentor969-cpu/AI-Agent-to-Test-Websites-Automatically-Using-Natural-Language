def run_agent(instruction: str):
    instruction = instruction.strip()

    if instruction == "":
        return {
            "status": "error",
            "message": "No instruction provided"
        }

    instruction_lower = instruction.lower()

    if "login" in instruction_lower:
        intent = "login_page_test"
    elif "search" in instruction_lower:
        intent = "search_page_test"
    else:
        intent = "generic_test"

    response = {
        "status": "success",
        "detected_intent": intent,
        "original_instruction": instruction
    }

    return response
