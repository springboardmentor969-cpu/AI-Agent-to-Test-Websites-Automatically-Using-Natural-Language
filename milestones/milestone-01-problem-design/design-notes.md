# Design Notes

## Architecture Decisions
- Flask is used as a lightweight backend framework to handle user requests
- A modular architecture is adopted to separate responsibilities
- Playwright is used for reliable and modern browser automation

## Module Description
- UI Layer: Accepts natural language input from the user
- NLP Parser: Interprets instructions and extracts actions
- Test Case Generator: Converts actions into Playwright scripts
- Executor: Runs tests in a headless browser
- Report Generator: Produces structured test results

## Data Flow
User Input → NLP Parser → Test Generator → Executor → Report Generator

## Advantages of the Design
- Clean separation of concerns
- Easy to maintain and extend
- Supports future enhancements such as CI/CD integration
