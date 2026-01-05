# # from reporting.report_writer import write_report

# # def generate_report(inp, parsed, steps, result, error, duration, screenshot):
# #     report = {
# #         "input": inp,
# #         "parsed": parsed,
# #         "steps": steps,
# #         "status": result,
# #         "error": error,
# #         "duration_seconds": duration,
# #         "screenshot": screenshot
# #     }
# #     path = write_report(report)
# #     report["report_file"] = path
# #     return report
# from reporting.history_store import add_history
# from reporting.report_writer import write_report

# def generate_report(inp, parsed, steps, result, error, duration, screenshot):
#     report = {
#         "input": inp, "parsed": parsed, "steps": steps,
#         "status": result, "error": error,
#         "duration_seconds": duration, "screenshot": screenshot
#     }
#     report["report_file"] = write_report(report)
#     add_history(report)
#     return report
from reporting.history_store import add_history
from reporting.report_writer import write_report

def generate_report(inp, parsed, steps, result, error, duration, screenshot):
    report = {
        "input": inp,
        "status": result,
        "steps": steps,
        "duration_seconds": duration,
        "error": error
    }
    report["report_file"] = write_report(report)
    add_history(report)
    return report
