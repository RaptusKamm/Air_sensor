import Settings
import calendar
from tkinter import *
import db
import matplotlib.pyplot as plt
from datetime import date
import Download_Data #Wird importiert, damit die Datei einmal ausgeführt wird. Downloadet alle CSVs bis zum letzten verfügbaren Tag, wenn nicht bereits schon ein Inhalt im Ordner CSVs enthalten ist

class Calendar:
    def __init__(self, root, year, month):
        self.year = year
        self.month = month
        self.cal = calendar.monthcalendar(self.year, self.month) #Gibt eine Liste mit mehreren kleinen Listen darin wieder, die die einzelnen Wochen beinhalten. Die 0 sind Tage von anderen Monaten (Werden dennoch ausgegeben, um eine Liste mit 7 Inhalten zu haben damit die Matrix vollständig ist)
        #Inhalt von self.cal im Januar = [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]

        self.root = root
        self.root.title("Sensor Data") #Titel des Fensters
        self.root.configure(background= Settings.background) #Setzen der Hintergrundfarbe
        self.root.geometry("500x500") #Setzen der Fenstergröße
        self.root.resizable(height= FALSE, width= FALSE) #Fenster soll nicht resizable sein
        
    def main(self):
        self.buttons() #Führt die Button Funktion aus. Muss in dieser Reihnfolge passieren, da sonst keine Buttons angezeigt werden
        self.root.mainloop() #Führt das main Fenster aus
    
    def buttons(self):
        self.body = Frame(self.root) #Ein Frame ist eine Art Struktur um eine Gruppe von mehreren Gegenständen an einem bestimmten Ort sortieren zu können
        self.body.configure(background= Settings.background) #Hintergrund des Frames wird auf Grau gesetzt, damit kein weißer Hintergrund vorhanden ist
        self.body.pack(side="top", pady= 110) #Der Frame wird ganz oben (top) platziert und dan mit pady um 110 Pixel nach unten verschoben, um es in der Mitte des Fensters zu haben

        self.month_name = Label(self.root, text = f"{calendar.month_name[self.month]} {self.year}") #self.root ist das Hauptfenster (Wird unten als Objekt erstellt), damit er weiß, wo er zu erscheinen hat
        self.month_name.place(x=205, y= 10)

        self.month_for = Button(self.root, text ="Month forward", command=self.next_month)
        self.month_for.place(x=300, y= 10)

        self.month_back = Button(self.root, text ="Month backward", command=self.last_month)
        self.month_back.place(x=100, y= 10)

        for weeks_num, week in enumerate(self.cal): #In weeks_num wird sich durch enumerate gemerkt in welcher Woche der Durchlauf gerade ist (z.B. Woche 2 von Januar) und in week sind dann die einzelnen Tage als Liste  - Also ähnliche Ausgabe wie bei self.cal nur werden die Listen einzelt abgehandelt
            for day_num, day in enumerate(week): #Es werden die einzelnen Tage in den Listen durchgegangen, diese sind dann einfach gelistet wie 1,2,3,4,5,6 etc.
                if day != 0: #Um ein Problem mit den Tagen aus anderen Monaten (Als 0 dargestellt) zu vermeiden, wird abgefragt, ob day keine 0 ist. Wenn ja, wird ein button erstellt
                    button = Button(self.body, text =day, height=2, width=4) #Der Button soll in dem erstellten body Frame angezeigt werden, als Inhalt den jeweiligen Tag haben und eine Höhe/Breite von 2/4 Pixeln haben
                    button.grid(row=weeks_num, column=day_num, padx=2, pady=2) #Dieser Button wird einem grid, also einer Anreihung von Buttons hinzugefügt. Dieses Grid hat in row die Anzahl von den jeweiligen weeks in einem Monat (+1 weg? / warum day_num? was bringt das) - padx/y = 2 beschreibt den Pixelabstand der Buttons zueinander
                    button.bind("<Button-1>", self.select) #Jeder Button bekommt eine Funktion gebinded, die ausgeführt werden soll, wenn mit Button-1 (Links Maus) draufgeklickt wird

    def next_month(self):
        if self.month == 12: #Wenn self.month 12 ist, soll es wieder auf 1 gesetzt werden und self.year um 1 erhöht werden
            self.month = 1
            self.year += 1
        else: #Ansonsten soll self.month um 1 erhöht werden
            self.month += 1
        self.cal = calendar.monthcalendar(self.year, self.month) #In self.cal wird ein Kalendar Schema gespeichert mit dem angegebenen Jahr und Monat
        self.month_name.config(text= f"{calendar.month_name[self.month]} {self.year}") #Dem Label self.month_name wird der Monatsname und das jeweilige Jahr übergeben, damit dies angezeigt wird
        widgets = self.body.grid_slaves() #Speichert eine Liste von allen Widgets in der Variable widgets
        for i in widgets:
            i.grid_forget() #i beinhaltet jeweils die einzelnen Widgets im Frame body. Diese "vergessen" durch grid_forget ihr grid, damit es danach neu aufgebaut werden kann, um das Fenster zu aktualiseren
        for weeks_num, week in enumerate(self.cal): #Die Buttons werden mit jedem neuen Monat neu erstellt, damit die Buttons dynamisch sind und Februar z.B. nur 28 Tage (2023) hat und nicht feste 31.
            for day_num, day in enumerate(week): 
                if day != 0: #Da mit self.cal gearbeitet wird, muss abgefragt werden, ob day eine 0 ist, weil self.cal eine Liste mit mehreren Wochen zurück gibt. Jede Woche hat immer 7 Tage. Wenn aber z.B. ein Monat erst am Donnerstag beginnt, sind alle vorherigen Tage aus dem Monat davor als 0 gekennzeichnet. Selbes mit Tagen im nächsten Monat.
                    button = Button(self.body, text =day, height=2, width=4)
                    button.grid(row=weeks_num, column=day_num, padx=2, pady=2)
                    button.bind("<Button-1>", self.select) #Ohne () wird die Funktion erst ausgeführt, wenn der Durchlauf hier angekommen ist. Mit () wird direkt beim ausführen des Codes die Funktion ausgeführt

    def last_month(self): #Selber Prozess wie bei next_month nur umgekehrt
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.cal = calendar.monthcalendar(self.year, self.month)
        self.month_name.config(text= f"{calendar.month_name[self.month]} {self.year}")
        print(self.month)
        widgets = self.body.grid_slaves()
        for i in widgets:
            i.grid_forget() #i beinhaltet jeweils die einzelnen Elemente im Frame body. Diese "vergessen" durch grid_forget ihr grid, damit es danach neu aufgebaut werden kann, um das Fenster zu aktualiseren
        for weeks_num, week in enumerate(self.cal):
            for day_num, day in enumerate(week): 
                if day != 0:
                    button = Button(self.body, text =day, height=2, width=4)
                    button.grid(row=weeks_num, column=day_num, padx=2, pady=2)
                    button.bind("<Button-1>", self.select)
    
    def select(self, event): #Funktion die die Buttons für die einzelnen Tage ausführen sollen, wenn sie angeklickt werden | event ist ein Parameter der von Tkinter bereitgestellt wird
        self.selected = event.widget #Prüft von welchen widget/button das Event ausgelöst wurde
        self.selected.config(relief="raised") #Es wird reagiert, wenn button losgelassen wird
        self.display_diagram()
    
    def display_diagram(self):
        self.date = date(self.year , self.month , self.selected.cget('text')) #text ist ein fester Parameter, der Zugriff auf den text des erstellen buttons gewährt (Um den Tag heraus zu bekommen)

        db_obj = db.Datenbank(self.date) #Erstellen eines Objekts der DB-Klasse
        data_fetch = db_obj.fetch_for_one_day() #In db.py

        self.P1_values = [row[0] for row in data_fetch] #row enthält mehrere Werte, P1, P2 und Datum. Hiermit wird sich nur der P1 Wert geholt
        self.P2_values = [row[1] for row in data_fetch] #Selbes hier mit dem P2 Wert

        plt.plot(self.P1_values, label='P1') # Erstellt zwei Linien, eine mit dem Label bzw. Namen P1 und eine mit dem Namen P2
        plt.plot(self.P2_values, label='P2')

        plt.ylim(0, 40) #Y-Achsen Werte von 0 bis 40
        plt.xticks(visible=False) #Auf der X-Achse sollen keine Werte angezeigt werden

        plt.xlabel('Datum') #Name der X-Achse ist Datum
        plt.ylabel('Werte') #Name der Y-Achse ist Datum
        plt.title(self.date) #Titel des Fensters ist das jeweilige Datum

        plt.legend() #Erstellt eine Legende die oben rechts angezeigt wird

        plt.show() #Lässt das neue Fenster mit dem Diagramm anzeigen


root = Tk()  # Root ist das Objekt der Klasse Tk (Kommt mit Tkinter), welches das Hauptfenster ist
cal = Calendar(root, Settings.year, Settings.month) #Bekommt root (Also das Mainfenster), das Jahr und den Monat übergeben

#obj = calendar.Calendar()

cal.main() #Führt die main Methode der Calendar-Klasse aus, die alles ins rollen bringt