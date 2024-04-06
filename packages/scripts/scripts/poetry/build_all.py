import os
import subprocess
from pathlib import Path
from scripts.utils.packages import get_package_paths

def build_package(directory: Path):
    print(f"Building package: {directory}")
    subprocess.run(["poetry", "build"], cwd=directory)


def build_all():
    root_path = Path(os.getcwd())
    
    print("Starting building of all packages...")
    
    package_paths = get_package_paths()
    for path in package_paths:
        build_package(path)

    print("Finished building all packages.")


if __name__ == "__main__":
    build_all()