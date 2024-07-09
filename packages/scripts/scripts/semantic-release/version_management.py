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
from semantic_release.cli import main as semantic_release_cli
from semantic_release.version import Version


def get_changed_packages() -> list[str]:
    result = subprocess.run(['git', 'diff', '--name-only', 'origin/main...HEAD'],
                            capture_output=True, text=True, check=False)
    changed_files = result.stdout.splitlines()

    changed_packages = set()
    for file in changed_files:
        if file.startswith(('packages/', 'services/')):
            package = '/'.join(file.split('/')[:2])
            changed_packages.add(package)
    root_package = os.getcwd()
    changed_packages.add(root_package)
    return list(changed_packages)


def determine_bump_type(package: str) -> str:
    os.chdir(package)
    current_version = Version(current=True)
    next_version = Version(current=True, next=True)
    os.chdir('../..')

    if next_version.major > current_version.major:
        return 'major'
    if next_version.minor > current_version.minor:
        return 'minor'
    return 'patch'


def bump_package_version(package: str) -> None:
    os.chdir(package)

    # Load package-specific configuration
    with open('pyproject.toml') as f:
        config = toml.load(f)

    version_variable = config['tool']['semantic_release']['version_variable']
    changelog_file = config['tool']['semantic_release']['changelog_file']

    bump_type = determine_bump_type(package)
    semantic_release_cli(['version', f'--{bump_type}', f'--version-variable={version_variable}', f'--changelog-file={changelog_file}'])

    os.chdir('../..')


def get_root_bump_type(changed_packages: list[str]) -> str:
    bump_type = 'patch'
    for package in changed_packages:
        if package['bump'] == 'major':
            return 'major'
        if package['bump'] == 'minor':
            bump_type = 'minor'
    return bump_type


def bump_root_version(changed_packages: list[str]) -> None:
    with open('pyproject.toml') as f:
        config = toml.load(f)

    current_version = config['tool']['poetry']['version']
    version = Version(current_version)

    bump_type = get_root_bump_type(changed_packages)
    if bump_type == 'major':
        new_version = version.next_major()
    elif bump_type == 'minor':
        new_version = version.next_minor()
    else:
        new_version = version.next_patch()

    config['tool']['poetry']['version'] = str(new_version)

    with open('pyproject.toml', 'w') as f:
        toml.dump(config, f)

    return str(new_version)


def main() -> None:
    changed_packages = get_changed_packages()
    for package in changed_packages:
        bump_package_version(package)
    bump_root_version(changed_packages)


if __name__ == "__main__":
    main()
