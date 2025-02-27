#!/usr/bin/env bash
# Exit on error
set -o errexit

#poetry install
pip install -r requirements.txt
#Este pip install -r requirements.txt es para instalar las dependencias que se encuentran en el archivo requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate