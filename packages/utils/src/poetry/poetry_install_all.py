import os
import subprocess
from pathlib import Path

excluded_directories = [".aws-sam"]
service_directories = ["services"]


def is_excluded(path: Path):
    return any(excluded_folder in path.parts for excluded_folder in excluded_directories)


def is_service_path(path: Path):
    return any(folder in path.parts for folder in service_directories)


def install_dependencies_in_directory(directory: Path):
    print(f"Installing dependencies in: {directory}")
    subprocess.run(["poetry", "install"], cwd=directory)


def export_requirements_to_directory(directory: Path):
    print(f"Exporting dependencies to: {directory}/requirments.txt")
    subprocess.run(["poetry", "export", "-f", "requirements.txt", "--output", "./requirements.txt", "--without-hashes"], cwd=directory)


def find_and_install_packages(start_directory: Path):
    for pyproject_path in start_directory.glob('**/pyproject.toml'):
        if not is_excluded(pyproject_path):
            install_dependencies_in_directory(pyproject_path.parent)
            if is_service_path(pyproject_path):
                export_requirements_to_directory(pyproject_path.parent)

# if __name__ == "__main__":
#     root_path = Path(os.getcwd())
#     print(f"Starting installation of all packages...")
#     find_and_install_packages(root_path)
#     print("Finished installing dependencies for all packages.")


def install_all():
    root_path = Path(os.getcwd())
    print("Starting installation of all packages...")
    find_and_install_packages(root_path)
    print("Finished installing dependencies for all packages.")
