import pathspec
import os
import subprocess

def load_gitignore(root_dir):
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            patterns = file.readlines()
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)

def get_changed_files(directory):
    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", "origin/main"],
        cwd=directory,
        text=True
    )
    return changed_files.splitlines()