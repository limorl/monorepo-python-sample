import os
import subprocess
from pathlib import Path

excluded_paths = [ ".aws-sam"]

def is_excluded(path: Path):
    return any(excluded_folder in path.parts for excluded_folder in excluded_paths)


def install_dependencies_in_directory(directory: Path):
    print(f"Installing dependencies in: {directory}")
    subprocess.run(["poetry", "install"], cwd=directory)

def find_and_install_packages(start_directory: Path):
    for pyproject_path in start_directory.glob('**/pyproject.toml'):
        if not is_excluded(pyproject_path):
            install_dependencies_in_directory(pyproject_path.parent)

# if __name__ == "__main__":
#     root_path = Path(os.getcwd())
#     print(f"Starting installation of all packages...")
#     find_and_install_packages(root_path)
#     print("Finished installing dependencies for all packages.")

def install_all():
    root_path = Path(os.getcwd())
    print(f"Starting installation of all packages...")
    find_and_install_packages(root_path)
    print("Finished installing dependencies for all packages.")