import os
import pathspec
import subprocess

from .packages import get_package_paths


def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            patterns = file.readlines()
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)


def find_packages_not_ignored(root_dir, spec):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if spec.match_file(dirpath):
            continue
        if "__init__.py" in filenames:
            yield dirpath

        # Remove ignored directories
        dirnames[:] = [d for d in dirnames if not spec.match_file(os.path.join(dirpath, d))]


def run_pytest_for_package(package_dir):
    if package_dir:
        subprocess.run(["pytest"], cwd=package_dir)


def main():
    package_paths = get_package_paths()
    for path in package_paths:
        print("Runnin Pytest for package: ", path)
        run_pytest_for_package(path)


if __name__ == "__main__":
    main()
