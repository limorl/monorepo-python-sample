import os
import subprocess
from pathlib import Path
from .packages import get_package_paths


def export_requirements_to_directory(directory: Path):
    print(f"Exporting dependencies to: {directory}/requirments.txt")
    subprocess.run(["poetry", "export", "-f", "requirements.txt", "--output", "./requirements.txt", "--without-hashes"], cwd=directory)


def export_requirements_all():
    root_path = Path(os.getcwd())
    print(f"Exporting requirements for all packages under ${root_path}...")
    
    package_paths = get_package_paths()
    for path in package_paths:
        export_requirements_to_directory(path)

    print("Finished exporting requirements for all packages.")


if __name__ == "__main__":
    export_requirements_all()
