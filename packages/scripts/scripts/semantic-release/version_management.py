"""
Basic implementation of version management.
Based on the commit message (conventional), the version of all updated packages should be bumped.
At this point, no distinction between actual chage type per package.

The version bump is managed by semantic_release as follows:
PATCH version bump: when the type is fix, refactor, style, or test
MINOR version bump: when the type is feat
MAJOR version bump: when there's a BREAKING CHANGE: footer, or the type is BREAKING CHANGE (regardless of the commit type)
"""

import os
import subprocess

import toml
from semantic_release import cli
from semantic_release.cli import changelog, version
from semantic_release.cli import main as semantic_release_cli
from semantic_release.version import Version


def get_changed_components() -> list[str]:
    result = subprocess.run(['git', 'diff', '--name-only', '$(git describe --tags --abbrev=0)'],
                            capture_output=True, text=True, check=False)
    changed_files = result.stdout.splitlines()

    changed_components = set()
    for file in changed_files:
        if file.startswith(('packages/', 'services/')):
            component = '/'.join(file.split('/')[:2])
            changed_components.add(component)

    return list(changed_components)


def determine_bump_type(component: str) -> str:
    os.chdir(component)
    current_version = Version(current=True)
    next_version = Version(current=True, next=True)
    os.chdir('../..')

    if next_version.major > current_version.major:
        return 'major'
    if next_version.minor > current_version.minor:
        return 'minor'
    return 'patch'


def bump_version(component: str) -> None:
    os.chdir(component)

    # Load package-specific configuration
    with open('pyproject.toml') as f:
        config = toml.load(f)

    version_variable = config['tool']['semantic_release']['version_variable']
    changelog_file = config['tool']['semantic_release']['changelog_file']

    bump_type = determine_bump_type(component)
    semantic_release_cli(['version', f'--{bump_type}', f'--version-variable={version_variable}', f'--changelog-file={changelog_file}'])

    os.chdir('../..')


def main() -> None:
    changed_components = get_changed_components()
    for component in changed_components:
        bump_version(component)


if __name__ == "__main__":
    main()
