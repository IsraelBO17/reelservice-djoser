# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py makemigrations

# Apply any outstanding database migrations
python manage.py migrate

# Create superuser 
python manage.py createsu

# Create groups
python manage.py creategroups
