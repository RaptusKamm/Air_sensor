import os

#Date
year, month = 2023, 1

#Colors
background = "grey"

#DB
absolute_csv_path = os.path.dirname(__file__)
relative_csv_path = "\CSVs"
csv_path = absolute_csv_path + relative_csv_path


absolute_db_path = os.path.dirname(__file__)
relative_db_path = "\sensor_db.db"
db_path = absolute_db_path + relative_db_path