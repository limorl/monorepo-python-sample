import sys
from scripts.poetry.install_all import install_all as install_all
from scripts.poetry.build_all import build_all as build_all


def run_script(script_name):
    match script_name:
        case "install_all":
            install_all()
        case "build_all":
            build_all();
        case _:
            print(f"Unknown script: {script_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poetry run poetry-script <script_name>")
    else:
        script_name = sys.argv[1]
        run_script(script_name)
