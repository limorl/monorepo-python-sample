import os
import subprocess

from scripts.utils.packages import get_package_paths
from scripts.utils.git import load_gitignore, get_changed_files
from typing import List, Any


def _is_python_file(file_path: str) -> bool:
    return file_path.endswith('.py')

def _get_test_file(file_path: str, package_paths: List[str]) -> str:
    file_name = os.path.basename(file_path)
    test_file_name_1 = file_name.replace('.py', '_test.py')
    test_file_name_2 =  f'test_{file_name}'

    for package_path in package_paths:
        if file_path.startswith(package_path):
            package_name = os.path.basename(package_path).replace('-','_')
            package_code_dir = os.path.join(package_path, package_name)
            package_test_dir = os.path.join(package_path, 'tests')

            test_file_path_1 = file_path.replace(package_code_dir, package_test_dir).replace(file_name, test_file_name_1)
            test_file_path_2 = file_path.replace(package_code_dir, package_test_dir).replace(file_name, test_file_name_2)

            if os.path.exists(test_file_path_1):
                return test_file_path_1
            if os.path.exists(test_file_path_2):
                return test_file_path_2

def _file_ignored(file_path: str, spec: Any) -> bool:
    dir_path = os.path.dirname(file_path)

    return spec.match_file(file_path) or spec.match_file(dir_path)


def get_impacted_test_files(changed_files: List[str], package_paths: List[str]) -> List[str]:
    impacted_test_files = []
  
    for file in changed_files:
        if file.endswith('_test.py') or file.startswith('test_'):
            impacted_test_files.append(file)
        else:
            test_file = _get_test_file(file, package_paths)
            if test_file:
                impacted_test_files.append(test_file)
    return impacted_test_files


def run_pytest_on_files(dir: str, files) -> List[str]:
    if files:
        subprocess.run(['pytest', '-vs', ' '.join(files) ], cwd=dir)


def _get_relative_path(full_path: str, relative_path: str) -> str:
    return os.path.relpath(full_path, relative_path)


def pytest_impacted_only():
    root_dir = os.getcwd()
    spec = load_gitignore(root_dir)
    package_paths = list(map(lambda x: _get_relative_path(str(x), root_dir), get_package_paths()))
    changed_py_files = list(filter(_is_python_file, get_changed_files(root_dir)))
    changed_py_files_not_ignored = list(filter(lambda x: not _file_ignored(x, spec), changed_py_files))

    impacted_test_files = get_impacted_test_files(changed_py_files_not_ignored, package_paths)

    if impacted_test_files:
        print(f'Running {len(impacted_test_files)} impacted tests under {root_dir}')
        run_pytest_on_files(root_dir, impacted_test_files)


if __name__ == "__main__":
    pytest_impacted_only()
