import os
from pathlib import Path

excluded_directories = [".aws-sam", "__pycache__"]
service_directories = ["services"]


def is_excluded(path: Path) -> bool:
    return any(excluded_folder in path.parts for excluded_folder in excluded_directories)


def is_service_path(path: Path) -> bool:
    return any(folder in path.parts for folder in service_directories)


def is_root_pyproject(path: Path) -> bool:
    root_path = Path(os.path.join(os.environ["PWD"], 'pyproject.toml'))
    return path == root_path


def get_package_paths() -> list[Path]:
    root_path = Path(os.getcwd())
    project_paths = root_path.glob('**/pyproject.toml')

    return [x.parent for x in project_paths if not is_excluded(x)]


if __name__ == "__main__":
    get_package_paths()
