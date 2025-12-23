def handle_instruction(instruction: str) -> str:
    """
    Baseline agent function.
    Currently echoes the instruction.
    Future versions will use LangGraph + Playwright.
    """

    if not instruction:
        return "No instruction provided."

    # Placeholder logic
    response = f"Agent received instruction: {instruction}"

    return response
