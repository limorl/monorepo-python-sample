import os
import subprocess
from pathlib import Path

excluded_directories = [".aws-sam", "__pycache__"]
service_directories = ["services"]


def is_excluded(path: Path):
    is_excluded = any(excluded_folder in path.parts for excluded_folder in excluded_directories)
    is_root = is_root_pyproject(path) # for now we are not treating the root as a package
    return is_excluded or is_root


def is_service_path(path: Path):
    return any(folder in path.parts for folder in service_directories)       


def is_root_pyproject(path: Path):
    root_path = Path(os.path.join(os.environ["PWD"], 'pyproject.toml'))
    return path == root_path


def get_package_paths():
    root_path = Path(os.getcwd())
    package_paths = []

    for pyproject_path in root_path.glob('**/pyproject.toml'):
        if not is_excluded(pyproject_path):
            package_paths.append(pyproject_path.parent)
    return package_paths


if __name__ == "__main__":
    get_package_paths()
