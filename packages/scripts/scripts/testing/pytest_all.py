import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from scripts.utils.packages import get_package_paths


def has_tests_folder(package_dir: Path) -> bool:
    return os.path.exists(os.path.join(package_dir, 'tests'))


def run_pytest_for_package(package_dir: Path, test_type: str) -> None:
    if package_dir and has_tests_folder(package_dir):
        if test_type == "all":
            subprocess.run(["pytest"], cwd=package_dir, check=False)
        elif test_type == 'unit':
            subprocess.run(["pytest", "-m", "not integration and not e2e"], cwd=package_dir, check=False)
        else:
            subprocess.run(["pytest", "-m", test_type], cwd=package_dir, check=False)


def pytest_all(test_type: str) -> None:
    package_paths = get_package_paths()
    for path in package_paths:
        print("Running Pytest for package: ", path)
        run_pytest_for_package(path, test_type)


def _create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(prog='pytest_all.py', description='Run all tests if given type using Pytest')
    parser.add_argument('--type', type=str, required=False, default='all',
                        help='The pytest mark to run [all|unit|integration|e2e]')
    return parser


def main() -> None:
    parser = _create_arg_parser()
    args = parser.parse_args()

    pytest_all(args.type)

if __name__ == "__main__":
    main()
