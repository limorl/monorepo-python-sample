import os
import subprocess
from pathlib import Path
from scripts.utils.packages import get_package_paths, is_service_path


def export_requirements_to_directory(directory: Path):
    print(f"Exporting dependencies to: {directory}/requirements.txt")
    subprocess.run(["poetry", "export", "-f", "requirements.txt", "--output", "./requirements.txt", "--without-hashes"], cwd=directory)


def install_dependencies_in_directory(directory: Path):
    print(f"Installing dependencies in: {directory}")
    subprocess.run(["poetry", "lock", "--no-update"], cwd=directory)
    subprocess.run(["poetry", "install"], cwd=directory)


def find_and_install_packages(start_directory: Path):
    package_paths = get_package_paths()
    for path in package_paths:
        install_dependencies_in_directory(path)
        if is_service_path(path):
            export_requirements_to_directory(path)


def install_all():
    root_path = Path(os.getcwd())
    print("Starting installation of all packages...")
    find_and_install_packages(root_path)
    print("Finished installing dependencies for all packages.")


if __name__ == "__main__":
    install_all()
