# Saves the labels as a fixture JSON file
python manage.py dumpdata --indent=4 --format=json -o recognition/fixtures/labels.json recognition
