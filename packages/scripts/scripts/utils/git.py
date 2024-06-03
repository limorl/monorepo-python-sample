import os
import subprocess

import pathspec


def load_gitignore(root_dir: str) -> None:
    gitignore_path = os.path.join(root_dir, '.gitignore')
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as file:
            patterns = file.readlines()
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns)


def get_changed_files(directory: str) -> list[str]:
    changed_files = subprocess.check_output(
        ["git", "diff", "--name-only", "origin/main"],
        cwd=directory,
        text=True
    )
    return changed_files.splitlines()
