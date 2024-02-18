from urllib import request
from calendar import Calendar
import Settings
from datetime import date, timedelta
import os

obj = Calendar()

class Downloader:
    def __init__(self):
        self.sensors = ['sds011_sensor_3659', 'sds011_sensor_36593']

        self.current_month = Settings.month
        self.current_year = Settings.year
        self.current_date = date.today()

    def download(self):
        while list(obj.itermonthdates(self.current_year, self.current_month))[0] < self.current_date: #Startet bei 2022-12-26
            tmp = obj.itermonthdates(self.current_year, self.current_month) #Datum mit dem immer hochgezählt wird
            for csv_date in tmp: #Wenn ein Durchlauf dieser Schleife beendet ist, wird in den nächsten Monate gegangen
                for sen in self.sensors:
                    if csv_date.month == self.current_month:
                        file_name = str(csv_date) + ".csv"
                        url = f"https://archive.sensor.community/{csv_date}/{csv_date}_{sen}.csv"

                        if os.path.exists("CSVs\\" + file_name) == False: #Wenn die Datei nicht existiert, soll sie gedownloadet werden
                            try: #Wenn try fehlschlägt, wird nicht abgebrochen
                                request.urlretrieve(url, f'CSVs/{file_name}')
                                print(url)
                            except Exception as e:
                                print(f"Error downloading: {url}")
                        else:
                            print("File already exist")

            print(tmp)
            self.current_month += 1
            if self.current_month > 12:
                self.current_month = 1
                self.current_year += 1

down_obj = Downloader()

down_obj.download()