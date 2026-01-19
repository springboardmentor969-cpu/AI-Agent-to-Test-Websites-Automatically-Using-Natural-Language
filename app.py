import subprocess
import sys
import os

def run_streamlit():
    ui_path = os.path.join("src", "ui.py")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", ui_path],
        check=True
    )

if __name__ == "__main__":
    print("Starting AI Website Testing Agent...")
    run_streamlit()
