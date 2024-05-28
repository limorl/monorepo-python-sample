import argparse
import os
from pathlib import Path
import pathspec
import subprocess

from scripts.utils.packages import get_package_paths


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


def has_tests_folder(package_dir):
    return os.path.exists(os.path.join(package_dir, 'tests'))


def run_pytest_for_package(package_dir: Path, type: str):
    if package_dir and has_tests_folder(package_dir):
        if type == "all":
            subprocess.run(["pytest"], cwd=package_dir)
        elif type == 'unit':
            subprocess.run(["pytest", "-m", "not integration and not e2e"], cwd=package_dir)
        else:
            subprocess.run(["pytest", "-m", type], cwd=package_dir)


def pytest_all(mark: str):
    package_paths = get_package_paths()
    for path in package_paths:
        print("Running Pytest for package: ", path)
        run_pytest_for_package(path, mark)


def _create_arg_parser():
    parser = argparse.ArgumentParser(prog='pytest_all.py', description='Run all tests if given type using Pytest')
    parser.add_argument('--type', type=str, required=False, default='all', help='The pytest mark to run [all|unit|integration|e2e]')
    return parser


if __name__ == "__main__":
    parser = _create_arg_parser()
    args = parser.parse_args()

    pytest_all(args.type)

