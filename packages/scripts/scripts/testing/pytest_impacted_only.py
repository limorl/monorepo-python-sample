import os
import pathspec
import subprocess


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


def git_changed_files(directory):
    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", "origin/main"],
        cwd=directory,
        text=True
    )
    return changed_files.splitlines()

# TODO @limorl: Fix to comply with new package structure
def identify_impacted_files(changed_files):
    impacted_files = []
    for file in changed_files:
        if file.endswith("_test.py") or file.endswith(".py"):
            impacted_files.append(file)
            if not file.endswith("_test.py"):
                test_file = file.replace(".py", "_test.py")
                if os.path.exists(test_file):
                    impacted_files.append(test_file)
    return impacted_files


def run_pytest_on_files(directory, files):
    if files:
        parent_directory = os.path.dirname(directory)
        print("Runnin tests on impacted files under: ", parent_directory)
        subprocess.run(["pytest"], cwd=parent_directory)


def main(root_dir):
    spec = load_gitignore(root_dir)
    for package in find_packages_not_ignored(root_dir, spec):
        changed_files = git_changed_files(package)
        impacted_files = identify_impacted_files(changed_files)
        run_pytest_on_files(package, impacted_files)


if __name__ == "__main__":
    root_dir = os.getcwd()
    main(root_dir)
