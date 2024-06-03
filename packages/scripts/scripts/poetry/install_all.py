import subprocess
from pathlib import Path

from scripts.utils.packages import get_package_paths, is_service_path


def export_requirements_to_directory(directory: Path) -> None:
    print(f'Exporting dependencies to: {directory}/requirements.txt')
    subprocess.run(
        ['poetry', 'export', '-f', 'requirements.txt', '--output', './requirements.txt', '--without-hashes'],
        cwd=directory,
        check=True,
    )


def install_dependencies_in_directory(directory: Path) -> None:
    print(f'Installing dependencies in: {directory}')
    subprocess.run(['poetry', 'lock', '--no-update'], cwd=directory, check=True)
    subprocess.run(['poetry', 'install'], cwd=directory, check=True)


def find_and_install_packages() -> None:
    package_paths = get_package_paths()
    for path in package_paths:
        install_dependencies_in_directory(path)
        if is_service_path(path):
            export_requirements_to_directory(path)


def install_all() -> None:
    print('Starting installation of all packages...')
    find_and_install_packages()
    print('Finished installing dependencies for all packages.')


if __name__ == '__main__':
    install_all()
