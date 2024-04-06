import subprocess
import sys

def run_script(script_name):
    poetry_path = "/usr/local/bin/poetry"
    command = f"{poetry_path} run {script_name}"
    try:
        subprocess.run(command, shell=True, check=True)
        # subprocess.run(command, shell=True, executable='/bin/bash', check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_script.py <script-name>")
    else:
        script_name = sys.argv[1]
        run_script(script_name)
