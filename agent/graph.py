# # # # from langgraph.graph import StateGraph
# # # # from parser.instruction_parser import parse_instruction, map_to_code

# # # # # Step 1: Parser Node
# # # # def parser_node(state):
# # # #     parsed = parse_instruction(state["input"])
# # # #     return {"parsed": parsed}

# # # # # Step 2: Code Generator Node
# # # # def generator_node(state):
# # # #     code = map_to_code(state["parsed"])
# # # #     return {
# # # #         "parsed": state["parsed"],
# # # #         "code": code
# # # #     }

# # # # # Create Graph
# # # # graph = StateGraph(dict)

# # # # graph.add_node("parser", parser_node)
# # # # graph.add_node("generator", generator_node)

# # # # graph.add_edge("parser", "generator")

# # # # graph.set_entry_point("parser")
# # # # graph.set_finish_point("generator")

# # # # app_graph = graph.compile()
# # # from langgraph.graph import StateGraph
# # # from parser.instruction_parser import parse_instruction
# # # from playwright_runner.code_generator import generate_playwright_code
# # # from playwright_runner.assertions import generate_assertion
# # # from playwright_runner.runner import run_test

# # # def parser_node(state):
# # #     parsed = parse_instruction(state["input"])
# # #     return {"parsed": parsed}

# # # def code_node(state):
# # #     code = generate_playwright_code(state["parsed"])
# # #     assertion = generate_assertion(state["parsed"])
# # #     return {
# # #         "parsed": state["parsed"],
# # #         "code": code,
# # #         "assertion": assertion
# # #     }

# # # def execute_node(state):
# # #     if not state["code"]:
# # #         return {"result": "No executable test generated"}

# # #     result = run_test(state["code"], state["assertion"])
# # #     return {
# # #         "parsed": state["parsed"],
# # #         "code": state["code"],
# # #         "assertion": state["assertion"],
# # #         "result": result
# # #     }

# # # graph = StateGraph(dict)

# # # graph.add_node("parser", parser_node)
# # # graph.add_node("code", code_node)
# # # graph.add_node("execute", execute_node)

# # # graph.add_edge("parser", "code")
# # # graph.add_edge("code", "execute")

# # # graph.set_entry_point("parser")
# # # graph.set_finish_point("execute")

# # # app_graph = graph.compile()

# # from langgraph.graph import StateGraph
# # from parser.instruction_parser import parse_instruction
# # from playwright_runner.code_generator import generate_playwright_code
# # from playwright_runner.assertions import generate_assertion
# # from playwright_runner.runner import run_test
# # from reporting.report_manager import generate_report

# # def parser_node(state):
# #     parsed = parse_instruction(state["input"])
# #     return {
# #         "input": state["input"],      # 👈 keep original input
# #         "parsed": parsed
# #     }

# # def code_node(state):
# #     return {
# #         "input": state["input"],      # 👈 propagate
# #         "parsed": state["parsed"],
# #         "code": generate_playwright_code(state["parsed"]),
# #         "assertion": generate_assertion(state["parsed"])
# #     }

# # def exec_node(state):
# #     if not state["code"]:
# #         return generate_report(state["input"], state["parsed"], [], "FAIL", "Invalid command", 0, None)

# #     result, steps, error, duration, screenshot = run_test(state["code"], state["assertion"])
# #     return generate_report(state["input"], state["parsed"], steps, result, error, duration, screenshot)

# # g = StateGraph(dict)
# # g.add_node("parser", parser_node)
# # g.add_node("code", code_node)
# # g.add_node("exec", exec_node)
# # g.add_edge("parser", "code")
# # g.add_edge("code", "exec")
# # g.set_entry_point("parser")
# # g.set_finish_point("exec")
# # app_graph = g.compile()
# from langgraph.graph import StateGraph
# from parser.instruction_parser import parse_instruction
# from playwright_runner.code_generator import generate_playwright_code
# from playwright_runner.assertions import generate_assertion
# from playwright_runner.runner import run_test
# from reporting.report_manager import generate_report

# def parser_node(state):
#     return {"input":state["input"],"headless":state["headless"],"parsed":parse_instruction(state["input"])}

# def code_node(state):
#     return {"input":state["input"],"headless":state["headless"],"parsed":state["parsed"],
#             "code":generate_playwright_code(state["parsed"]),
#             "assertion":generate_assertion(state["parsed"])}

# def exec_node(state):
#     if not state["code"]:
#         return generate_report(state["input"],state["parsed"],[],"FAIL","Invalid Command",0,None)
#     r,steps,err,dur,shot=run_test(state["code"],state["assertion"],state["headless"])
#     return generate_report(state["input"],state["parsed"],steps,r,err,dur,shot)

# g=StateGraph(dict)
# g.add_node("parser",parser_node)
# g.add_node("code",code_node)
# g.add_node("exec",exec_node)
# g.add_edge("parser","code")
# g.add_edge("code","exec")
# g.set_entry_point("parser")
# g.set_finish_point("exec")
# app_graph=g.compile()
from langgraph.graph import StateGraph
from parser.instruction_parser import parse_instruction
from playwright_runner.code_generator import generate_playwright_code
from playwright_runner.assertions import generate_assertion
from playwright_runner.runner import run_test
from reporting.report_manager import generate_report

def parser_node(state):
    return {
        "input": state["input"],
        "headless": state["headless"],
        "parsed": parse_instruction(state["input"])
    }

def code_node(state):
    return {
        **state,
        "code": generate_playwright_code(state["parsed"]),
        "assertion": generate_assertion(state["parsed"])
    }

def exec_node(state):
    if state["parsed"]["action"] == "invalid":
        return generate_report(
            state["input"], state["parsed"],
            [], "FAIL", "Invalid Command", 0, None
        )

    status, steps, error, duration, screenshot = run_test(
        state["code"], state["assertion"], state["headless"]
    )

    return generate_report(
        state["input"], state["parsed"],
        steps, status, error, duration, screenshot
    )

g = StateGraph(dict)
g.add_node("parser", parser_node)
g.add_node("code", code_node)
g.add_node("exec", exec_node)
g.add_edge("parser", "code")
g.add_edge("code", "exec")
g.set_entry_point("parser")
g.set_finish_point("exec")

app_graph = g.compile()
