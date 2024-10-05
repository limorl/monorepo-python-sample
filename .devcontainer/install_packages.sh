#!/bin/bash
set -ex


poetry config virtualenvs.in-project true

poetry lock --no-update # must run this line in order to install scripts and install-all command

poetry install --no-interaction --no-ansi

poetry run install-all

echo "Installing packages... Completed succfully!"