#!/bin/bash
# Exit on error
set -o e

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install --no-cache-dir -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate