# # import json, os, time
# # from datetime import datetime

# # REPORT_DIR = "reports"

# # def write_report(data):
# #     os.makedirs(REPORT_DIR, exist_ok=True)
# #     name = datetime.now().strftime("report_%d%m%Y_%H%M%S.json")
# #     path = os.path.join(REPORT_DIR, name)

# #     with open(path, "w") as f:
# #         json.dump(data, f, indent=4)

# #     return path
# import json,os,time
# os.makedirs("reports",exist_ok=True)

# def write_report(data):
#     path=f"reports/report_{int(time.time())}.json"
#     with open(path,"w") as f:
#         json.dump(data,f,indent=4)
#     return path
import json, time, os

def write_report(report):
    os.makedirs("reports", exist_ok=True)
    filename = f"report_{int(time.time())}.json"
    path = os.path.join("reports", filename)

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    return filename
