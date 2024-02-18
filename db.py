import sqlite3
from sqlite3 import Error
import Settings
import os
import csv

class Datenbank:
    def __init__(self, date):
        self.conn = sqlite3.connect(Settings.db_path) #Versucht eine Verbindung zu der DB auf Pfad "D:\ITF\LF05 (Alef)\Sensor\sensor_db.db" herzustellen (Wenn keine DB unter diesem Namen existiert, wird automatische eine neue angelegt)
        self.cur = self.conn.cursor() #Es wird ein Objekt erstellt, mit dem SQL Statements ausgeführt werden können
        self.schema() #Führt die Funktion schema() aus, die einen Table mit den entsprechenden Spalten (P1, P2, Datum) erzeugt
        self.data2db() #Da beim ausführen von Sensor_data_v1 die Datei Download_Data importiert wurde, werden direkt CSV-Datein gedownloadet. Erst später im Code wird das DB-Objekt erzeugt, wodurch der Code ausführbar ist. Wenn eine CSV-Daten vorhanden wären, bevor diese Funktion ausgeführt wird, kann nichts in die DB geschrieben werden
        self.date = date #date wurde in Sensor_data_v1 dem Objekt der Klasse Datenbank mitübergeben und enthält das aktuell gebrauchte Datum

    def schema(self):
        try:
            self.cur.execute('''
            CREATE TABLE sensor_data(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    P1 REAL,
                    P2 REAL,
                    date TEXT
            )''')
            print("Database created successfully!")
            self.conn.commit()
            print("Verbindung hergestellt")
        except Error as e:
            print(e)

    def close_connection(self): #Funktion um die Verbindung, falls nötig, zu schließen
        self.conn.close()
    
    def data2db(self):
        self.cur.execute('SELECT COUNT(*) FROM sensor_data')
        count = self.cur.fetchone()[0]
        if count == 0:
            for file in os.listdir(Settings.csv_path):
                with open(Settings.csv_path + "/" + file, "r") as file:
                    csv_reader = csv.reader(file, delimiter=';')
                    for row in csv_reader:
                        self.cur.execute(f'INSERT INTO sensor_data (P1, P2, date) VALUES (?, ?, ?)', (row[6], row[9], row[5]))
                print("Values added")
                self.conn.commit()
    
    def fetch_for_one_day(self): #Holt mit dem SQL Statement alle P1, P2 und Datum Daten vom jeweiligen Tag (self.date) - self.date ist ein Parameter der dem DB-Objekt in der main Datei übergeben wurde, da die Variable dort die Tage hochzählt
        self.cur.execute(f"SELECT P1, P2, date FROM sensor_data WHERE date LIKE '{self.date}%'")
        data_for_date = self.cur.fetchall()
        return data_for_date