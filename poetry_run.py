import sys
from packages.utils.src.poetry.poetry_install_all import install_all as install_all


def run_script(script_name):
    if script_name == "install_all":
        install_all()
    else:
        print(f"Unknown script: {script_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poetry run poetry-script <script_name>")
    else:
        script_name = sys.argv[1]
        run_script(script_name)
