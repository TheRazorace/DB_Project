# -*- coding: utf-8 -*-

import pymysql as sql
import pymysql.cursors as cur
import pandas as pd
import tkinter as tk
from tabulate import tabulate

#Σύνδεση στην βάση δεδομένων
def ConnectDatabase():
    
    connection = sql.connect (host = "150.140.186.221",
                  port = 3306,
                  user = "db20_up1047398",
                  password = "up1047398",
                  db = "project_db20_up1047398",
                  charset = "utf8mb4",
                  cursorclass=cur.DictCursor)
    
    connection.autocommit(True)
    
    #Δείκτης βάσης
    cursor = connection.cursor()  
    
    return cursor

#Ρύθμιση του Gui με κλάση
class Gui():
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    #Ορισμός παραθύρου
        self.window = tk.Tk()
        self.window.geometry('1350x650')
        self.window.title("Σύστημα Μεταφοράς Ηλεκτρικής Ενέργειας")
    
    #Τίτλος
        self.title_lbl = (tk.Label(self.window,  font=("Arial Bold", 15),
        text="""Επιλέξτε τα δεδομένα που επιθυμείτε να αναζητήσετε! """))
        self.title_lbl.place(x=420, y=10)  
    
    #Κουμπιά των queries (αυτά που είναι στην μέση)
        self.query1 = tk.Button(self.window)   
        self.query2 = tk.Button(self.window)   
        self.query3 = tk.Button(self.window)   
        self.query4 = tk.Button(self.window)   
        self.query5 = tk.Button(self.window) 
     
    #DropDown menus
        #Dates
        options1 = ["2015", "2016", "2017", "2018", "2019", "2020"]
        self.clicked = tk.StringVar()
        self.clicked.set("2015")
        self.dropmn1 = tk.OptionMenu(self.window, self.clicked, *options1)

        # Stations
        options2 = ["Αιολικός Σταθμός Ροδίνης", "Αιολικός Πάρκο Παναχαικού","Αιολικό Πάρκο Ναυπάκτου"]
        self.clicked2 = tk.StringVar()
        self.clicked2.set("Αιολικός Σταθμός Ροδίνης")
        self.dropmn2 = tk.OptionMenu(self.window, self.clicked2, *options2)

        #Time

        options3 = ["12:00:00", "12:15:00", "12:30:00", "12:45:00"]
        self.clicked3 = tk.StringVar()
        self.clicked3.set("12:00:00")
        self.dropmn3 = tk.OptionMenu(self.window, self.clicked3, *options3)
        
        #Εταιρείες ΑΠΕ

        options4 = ["AENAOS", "ALEXAKIS Energy", "Conergy", "Copelouzos","Damco Energy","kIEFER TEK","MES ENERGY",
                    "MP ENERGY", "ΕΛΤΕΧ ΑΝΕΜΟΣ", "ΕΝΤΕΚΑ" , "ΤΕΡΝΑ"]
        self.clicked4 = tk.StringVar()
        self.clicked4.set("AENAOS")
        self.dropmn4 = tk.OptionMenu(self.window, self.clicked4, *options4)
    
    #Labels που ίσως χρειαστούν
        self.label1 = tk.Label(self.window, font=("Arial", 7))
        self.label2 = tk.Label(self.window, font=("Arial", 7))
        self.label3 = tk.Label(self.window, font=("Arial", 7))
        self.label4 = tk.Label(self.window, font=("Arial", 7))
        self.label5 = tk.Label(self.window, font=("Arial", 7))
        
    #Inputs που ίσως χρειαστούν
        self.input1 = tk.Entry(self.window, width=20)
        self.input2 = tk.Entry(self.window, width=20)
        self.input3 = tk.Entry(self.window, width=20)
        self.input4 = tk.Entry(self.window, width=20)
        self.input5 = tk.Entry(self.window, width=20)
    
    #Πεδίο προβολής απαντήσεων (στα δεξιά)
        self.results = (tk.Label(self.window, font=("Consolas", 9),
                        justify=tk.LEFT, anchor='nw'))
        self.results.place(x=610, y=180)  
        self.results_title = tk.Label(self.window, font=("Arial", 12))  
        self.results_title.place(x=610, y=120)           
    
    #Κουμπιά επιλογής κατηγορίας ερώτησης (στα αριστερά)
        self.btn1 = (tk.Button(self.window, text="Διεσπαρμένη Παραγωγή",
        command = lambda: ProductionQueries(self)))
        self.btn1.place(x=25, y=180)
    
        self.btn2 = (tk.Button(self.window, text="Μετρήσεις Παραγωγής",
        command = lambda: ProductionStatsQueries(self)))
        self.btn2.place(x=25, y=260)
    
        self.btn3 = (tk.Button(self.window, text="Εταιρείες Παραγωγής",
        command = lambda: CompaniesQueries(self)))
        self.btn3.place(x=25, y=340)
    
        self.btn4 = (tk.Button(self.window, text="Κατανάλωση Περιοχών",
        command = lambda: AreaQueries(self)))
        self.btn4.place(x=25, y=420)
    
        self.btn5 = (tk.Button(self.window, text="Μέτρηση Κατανάλωσης",
        command = lambda: ConsumptionStatsQueries(self)))
        self.btn5.place(x=25, y=500)
    
        self.btn6 = (tk.Button(self.window, text="Τοπικοί Υποσταθμοί",
        command = lambda: SubstationQueries(self)))
        self.btn6.place(x=25, y=580)
    
        self.window.mainloop()
    

#Εκκίνηση gui με στιγμιότυπο της κλάσης
def StartMenu(cursor):
    
    gui = Gui(cursor)
    
    return

#Κατηγορίες queries
#Κάθε κουμπί στα δεξιά οδηγεί σε μία από τις κατηγορίες των queries
#Σε κάθε query κουμπί ρυθμίζεται εκ νέου το κείμενό του και η συνάρτηση που καλεί
#Σε κάθε query κουμπί ρυθμίζεις τι θες να έχουν μέσα τα labels και τα inputs
#με την εντολή configure. Αλλιώς τα κάνεις place_forget() για να μην φαίνονται

# Queries Διεσπαρμένης Παραγωγής
def ProductionQueries(gui):
    ClearGui(gui)

    gui.query1.configure(text="Σταθμοί παραγωγής Διεσπαρμένης Ενέργειας",
    command=lambda: Diesp1(gui))
    gui.query1.place(x=280, y=180)

    gui.query2.configure(text="Αρ. Σταθμών ΑΠΕ ανά Νομό",
    command=lambda: Diesp2(gui))
    gui.query2.place(x=280, y=260)

    gui.query3.configure(text="Είδη Ανανεώσιμης Ενέργειας ανά Νομό",
    command=lambda: Diesp3(gui))
    gui.query3.place(x=280, y=340)

    gui.query4.configure(text="Ενεργοί Σταθμοί έως:",
    command=lambda: Diesp4(gui))
    gui.query4.place(x=280, y=420)
    gui.dropmn1.place(x=420, y=420)

    gui.query5.configure(text="Επιλογή Σταθμού",
    command=lambda: Diesp5(gui))
    gui.query5.place(x=280, y=500)
    gui.dropmn2.place(x=405, y=500)


    return

#Queries Μέτρησης Παραγωγής
def ProductionStatsQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Παραγωγή Ανά Τέταρτο ",
    command=lambda: Production1(gui))
    gui.query1.place(x=280, y=180)
    gui.dropmn3.place(x=450, y=180)
    
    gui.query2.configure(text = "Συνολική  παραγωγή Σταθμών ανά ώρα ",
    command = lambda: Production2(gui))
    gui.query2.place(x=280, y=260)
    
    gui.query3.configure(text = "Μέση  παραγωγή ανά 15 min  ανά σταθμό",
    command=lambda: Production3(gui))
    gui.query3.place(x=280, y=340)
    
    gui.query4.configure(text = "Ποσοστό Προέλευσης Ενέργειας ",
    command=lambda: Production4(gui))
    gui.query4.place(x=280, y=420)
    
    gui.query5.configure(text = "Query μέτρησης παρ. 5")
    gui.query5.place(x=280, y=500)
    
    
    return

#Queries Εταιρειών
def CompaniesQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Ονόματα και Έδρες Εταιρειών ΑΠΕ ",
    command = lambda: Etaireia1(gui))
    gui.query1.place(x=280, y=180)
    
    gui.query2.configure(text = "Ταξινόμηση Εταιρειών με φθίνοντα Αριθμό Έργων ",
    command=lambda: Etaireia2(gui))
    gui.query2.place(x=280, y=260)
    
    gui.query3.configure(text = "Ταξινόμηση Εταιρειών με φθίνοντα Αριθμό Συνολικής Ισχύος σε MW ",
    command=lambda: Etaireia3(gui))
    gui.query3.place(x=280, y=340)
    
    gui.query4.configure(text = "Εταιρείες με τα 5 μεγαλύτερα έργα ",
    command = lambda: Etaireia4(gui))
    gui.query4.place(x=280, y=420)
    
    gui.query5.configure(text = "Όνομα Εταιρείας",
    command=lambda: Etaireia5(gui))
    gui.query5.place(x=280, y=500)
    gui.dropmn4.place(x=400, y=500)
    
    return


#Queries Περιοχών Κατανάλωσης
def AreaQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Περιοχές βάσει συμβολαίων",
    command = lambda: AreaAllContracts(gui))
    gui.query1.place(x=280, y=180)    
    gui.label1.configure(text="Πλήθος εμφάνισης: ")
    gui.label1.place(x=280, y=210)
    gui.input1.insert(10, 10)
    gui.input1.place(x=370, y=210)
    
    gui.query2.configure(text = "Περιοχές βάσει βιομηχανικών συμβολαίων",
    command = lambda: AreaIndustrialContracts(gui))
    gui.query2.place(x=280, y=260)   
    gui.label2.configure(text="Πλήθος εμφάνισης: ")
    gui.label2.place(x=280, y=290)
    gui.input2.insert(10, 10)
    gui.input2.place(x=370, y=290)
    
    gui.query3.configure(text = "Περιοχές βάσει αγροτικών συμβολαίων",
    command = lambda: AreaAgriContracts(gui))
    gui.query3.place(x=280, y=340)
    gui.label3.configure(text="Πλήθος εμφάνισης: ")
    gui.label3.place(x=280, y=370)
    gui.input3.insert(10, 10)
    gui.input3.place(x=370, y=370)
    
    
    gui.query4.configure(text = "Τοπικός υποσταθμός περιοχής",
    command = lambda: AreaStation(gui))
    gui.query4.place(x=280, y=420)
    gui.label4.configure(text="Περιοχή αναζήτησης: ")
    gui.label4.place(x=280, y=450)
    gui.input4.insert(10, 'Πάτρα - Κέντρο')
    gui.input4.place(x=375, y=450)
    
    #gui.query5.configure(text = "Query περιοχής 5")
    #gui.query5.place(x=350, y=500)   
    
    return

#Queries Μέτρησης Παραγωγής
def ConsumptionStatsQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Query μέτρησης κατ. 1")
    gui.query1.place(x=280, y=180)
    
    gui.query2.configure(text = "Query μέτρησης κατ. 2")
    gui.query2.place(x=280, y=260)
    
    gui.query3.configure(text = "Query μέτρησης κατ. 3")
    gui.query3.place(x=280, y=340)
    
    gui.query4.configure(text = "Query μέτρησης κατ. 4")
    gui.query4.place(x=280, y=420)
    
    gui.query5.configure(text = "Query μέτρησης κατ. 5")
    gui.query5.place(x=280, y=500)
    
    return

#Queries Υπόσταθμων Παραγωγής
def SubstationQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Σταθμοί χαμηλής τάσης",
    command = lambda: CommonStations(gui))
    gui.query1.place(x=280, y=180)
    gui.label1.configure(text="Πλήθος εμφάνισης: ")
    gui.label1.place(x=280, y=210)
    gui.input1.insert(10, 10)
    gui.input1.place(x=370, y=210)
    
    gui.query2.configure(text = "Σταθμοί εργοστασιακής χρήσης",
    command = lambda: IndustrialStations(gui))
    gui.query2.place(x=280, y=260)
    gui.label2.configure(text="Πλήθος εμφάνισης: ")
    gui.label2.place(x=280, y=290)
    gui.input2.insert(10, 10)
    gui.input2.place(x=370, y=290)
    
    gui.query3.configure(text = "Πλήθος πελατών εξυπηρέτησης σταθμών",
    command = lambda: StationsSort(gui))
    gui.query3.place(x=280, y=340)
    gui.label3.configure(text="Πλήθος εμφάνισης: ")
    gui.label3.place(x=280, y=370)
    gui.input3.insert(10, 10)
    gui.input3.place(x=370, y=370)
    
    gui.query4.configure(text = "Στοιχεία σύνδεσης σταθμών",
    command = lambda: NetworkConnections(gui))
    gui.query4.place(x=280, y=420)
    gui.label4.configure(text="Πλήθος εμφάνισης: ")
    gui.label4.place(x=280, y=450)
    gui.input4.insert(10, 10)
    gui.input4.place(x=370, y=450)
    
    #gui.query5.configure(text = "Query υπάσταθμου 5")
    #gui.query5.place(x=350, y=500)
    
    return

#Καθαρισμός οθόνης
def ClearGui(gui):
    
    #Κρύψιμο των κουμπιών
    gui.query1.place_forget()
    gui.query2.place_forget()
    gui.query3.place_forget()
    gui.query4.place_forget()
    gui.query5.place_forget()
    
    #Κρύψιμο των labels από άλλα κουμπιά
    gui.label1.place_forget()
    gui.label2.place_forget()
    gui.label3.place_forget()
    gui.label4.place_forget()
    gui.label5.place_forget()
    
    #Κρύψιμο των Drop Menus
    gui.dropmn1.place_forget()
    gui.dropmn2.place_forget()
    gui.dropmn3.place_forget()
    gui.dropmn4.place_forget()
    
    
    #Κρύψιμο των inputs από άλλα κουμπιά
    gui.input1.place_forget()
    gui.input2.place_forget()
    gui.input3.place_forget()
    gui.input4.place_forget()
    gui.input5.place_forget()
    
    #Διαγραφή περιεχομένου των inputs
    gui.input1.delete(0, tk.END)
    gui.input2.delete(0, tk.END)
    gui.input3.delete(0, tk.END)
    gui.input4.delete(0, tk.END)
    gui.input5.delete(0, tk.END)
    
    #Τα κουμπιά να μη δείχνουν σε κάποια συνάρτηση
    gui.query1.configure(command = lambda: None)
    gui.query2.configure(command = lambda: None)
    gui.query3.configure(command = lambda: None)
    gui.query4.configure(command = lambda: None)
    gui.query5.configure(command = lambda: None)
    
    #Κρύψιμο αποτελεσμάτων
    gui.results.configure(text = "")
    gui.results_title.configure(text ="")
    gui.results.configure(font = ("Consolas", 9))
    
    return



## Queries για  πίνακα Διεσπαρμένη Ενέργεια

def Diesp1(gui):  # Προβολή Σταθμών ανά Νομό με φθίνοντα αριθμό Ισχύος
    query = "SELECT `Νομός`, `Όνομα Σταθμού`  , `Εγκατεστημένη Ισχύς (MW)` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "ORDER BY `Νομός` ASC ,`Όνομα Σταθμού`  ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα")
    gui.results.configure(text=tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Diesp2(gui):  # Αριθμός Σταθμών ΑΠΕ ανά Νομό
    query = "SELECT `Νομός`, COUNT(`ID Μονάδας Παραγωγής`) as `Αρ. Μονάδσων Διεσπαρμένης Παραγωγής` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "GROUP BY `Νομός` " \
            "ORDER BY `Αρ. Μονάδσων Διεσπαρμένης Παραγωγής` DESC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα")
    gui.results.configure(text=tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Diesp3(gui):  # Αριθμός Σταθμών ΑΠΕ ανά Νομό
    query = "SELECT  COUNT(`Ενέργεια`) as `Αριθμός Μονάδων` ,`Ενέργεια` ,`Νομός`  " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "GROUP BY `Ενέργεια` , `Νομός` " \
            "ORDER BY `Νομός` ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα")
    gui.results.configure(text=tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Diesp4(gui):
    query = "SELECT   `Όνομα Σταθμού` ,`Ενέργεια` ,`Νομός` ,`Εγκατεστημένη Ισχύς (MW)` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "WHERE   YEAR(`Ενεργός Από:`) <= %s  " \
            "ORDER BY `Νομός` ASC  "
    ExecuteQuery_IntInput(query, gui.clicked.get(), gui)

def Diesp5(gui):  # Πληροφορίες Σταθμού
    query = "SELECT  `Νομός`, `Όνομα Σταθμού`  , `Εγκατεστημένη Ισχύς (MW)`  " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "WHERE `Όνομα Σταθμού` = %s  "
    ExecuteQuery_StrInput(query, gui.clicked2.get(), gui)
    return

## Queries για  πίνακα Εταιρείες

def Etaireia1(gui):    #Προβολή στοιχείων εταιρείας
    query = "SELECT DISTINCT  `Όνομα Εταιρείας` , `Έδρα Εταιρείας` " \
            "FROM `Εταιρεία` " \
            "ORDER BY `Έδρα Εταιρείας` ,`Όνομα Εταιρείας`  ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
    return

def Etaireia2(gui):   #Ταξινόμηση εταιρειών με βάση τον αριθμό έργων
    query = "SELECT `Όνομα Εταιρείας` ,COUNT('ID Διεσπαρμένης Παραγωγής')  as `Αριθμός Έργων` " \
            "FROM `Εταιρεία`" \
            "GROUP  BY `Όνομα Εταιρείας` " \
            "ORDER BY `Αριθμός Έργων` DESC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
    return

def Etaireia3(gui):  #Ταξινόμηση εταιρειών με βάση τα συνολικά έργα
    query = "SELECT `Όνομα Εταιρείας`  ,SUM(`Εγκατεστημένη Ισχύς (MW)`) as `Συνολική Ισχύς Έργων`  " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "GROUP BY `Όνομα Εταιρείας`" \
            "ORDER BY `Συνολική Ισχύς Έργων` DESC , `Όνομα Εταιρείας`   "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
    return

def Etaireia4(gui): #Ταξινόμηση ανα έργο ίσως και ανα περιοχή ??
    query = "SELECT `Όνομα Εταιρείας` , `Εγκατεστημένη Ισχύς (MW)` , `Ενέργεια` " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "ORDER BY `Εγκατεστημένη Ισχύς (MW)` DESC , `Όνομα Εταιρείας` " \
            "LIMIT 5  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Etaireia5(gui):  # Ταξινόμηση ανα έργο ίσως και ανα περιοχή ??
    query = "SELECT `Όνομα Σταθμού`,`Εγκατεστημένη Ισχύς (MW)` , `Ενέργεια` , `Νομός` " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "WHERE `Όνομα Εταιρείας`=%s " \
            "ORDER BY `Εγκατεστημένη Ισχύς (MW)` DESC  " \
            "LIMIT 5  "
    ExecuteQuery_StrInput(query, gui.clicked4.get(), gui)

    return


## Queries για  πίνακα Μετρήσεις Παραγωγής

def Production1(gui): #Μέγιστη παραγωγή ανά 15 min
    query = "SELECT `Συνολική Μέτρηση (KWh)` , `Όνομα Σταθμού` " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "WHERE TIME(`Ώρα`) = %s " \
            "ORDER BY `Συνολική Μέτρηση (KWh)` DESC "
    ExecuteQuery_StrInput(query, gui.clicked3.get(), gui)
    
    return


def Production2(gui): #Συνολική  παραγωγή ανά 1 hour  ανά σταθμό
    query = "SELECT SUM(`Συνολική Μέτρηση (KWh)`) as  `Συνολική Παραγωγή / h`,`Διεσπαρμένη Παραγωγή`.`Όνομα Σταθμού`  " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`" \
            "ORDER BY `Συνολική Παραγωγή / h` DESC "

    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Production3(gui): #Μέση  παραγωγή ανά 15 min  ανά σταθμό
    query = "SELECT AVG(`Συνολική Μέτρηση (KWh)`) as  `Συνολική Παραγωγή / 15 min`,`Διεσπαρμένη Παραγωγή`.`Όνομα Σταθμού`  " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`" \
            "ORDER BY `Συνολική Παραγωγή / 15 min` DESC "

    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

def Production4(gui): #Ποσοστό Προέλευσης Ενέργειας
    query = "SELECT SUM(`Συνολική Μέτρηση (KWh)`)/(SELECT SUM(`Μέτρηση Παραγωγής`.`Συνολική Μέτρηση (KWh)`) FROM `Μέτρηση Παραγωγής` ) as `Ποσοστό Συνολικής Παραγωγής`" \
            ",`Διεσπαρμένη Παραγωγή`.`Ενέργεια`  as `Είδος Ενέργειας ` " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Διεσπαρμένη Παραγωγή`.`Ενέργεια`" \
            "ORDER BY `Διεσπαρμένη Παραγωγή`.`Ενέργεια` ASC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)   
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))

    return

#Queries Κατανάλωσης Περιοχής
def AreaAllContracts(gui):
    
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`,
            SUM(`Οικιακά Συμβόλαια`) + SUM(`Εταιρικά Συμβόλαια`) + 
            SUM(`Βιομηχανικά Συμβόλαια`) + SUM(`Αγροτικά Συμβόλαια`) AS `Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Συμβόλαια` DESC
            LIMIT %s """
    
    ExecuteQuery_IntInput(query, gui.input1.get(), gui)
       
    return

def AreaIndustrialContracts(gui):
    
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`, `Βιομηχανικά Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Βιομηχανικά Συμβόλαια` DESC
            LIMIT %s"""
    
    ExecuteQuery_IntInput(query, gui.input2.get(), gui)
       
    return

def AreaAgriContracts(gui):
    
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`, `Αγροτικά Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Αγροτικά Συμβόλαια` DESC
            LIMIT %s"""
            
    ExecuteQuery_IntInput(query, gui.input3.get(), gui)
        
    return

def AreaStation(gui):
    
    query = """SELECT kp.`Περιοχή`,kp.`Τ.Κ.`, ty.`Όνομα Σταθμού` AS `Βασικός Υποσταθμός Περιοχής` 
            FROM `Κατανάλωση Περιοχής` kp 
            JOIN `Τοπικός Υποσταθμός` ty ON kp.`ID Βασικού Υποσταθμού` = ty.`ID Υποσταθμού`
            WHERE `Περιοχή` = %s"""
            
    entry = gui.input4.get()
    gui.cursor.execute(query, entry)
    data=cursor.fetchall()
    df = pd.DataFrame(data)
    
    PrintResults(gui, df)

    
#Queries Τοπικού Υποσταθμού
def CommonStations(gui):
    
    query = """SELECT `Όνομα Σταθμού`,`Γεωγρ. Μήκος`,`Γεωγρ. Πλάτος`,`Ενεργός Από` 
            FROM `Τοπικός Υποσταθμός` 
            WHERE `Μετασχηματισμός Τάσης` = '20KV/400V'
            LIMIT %s"""
     
    gui.results.configure(font = ("Consolas", 10))        
    ExecuteQuery_IntInput(query, gui.input1.get(), gui)
    
    return

def IndustrialStations(gui):
    
    query = """SELECT `Όνομα Σταθμού`,`Γεωγρ. Μήκος`,`Γεωγρ. Πλάτος`,`Ενεργός Από` 
            FROM `Τοπικός Υποσταθμός` 
            WHERE `Μετασχηματισμός Τάσης` != '20KV/400V'
            LIMIT %s"""
    
    gui.results.configure(font = ("Consolas", 10))
    ExecuteQuery_IntInput(query, gui.input2.get(), gui)
    
    return

def StationsSort(gui):
    
    query = """SELECT ty.`Όνομα Σταθμού`, ty.`Γεωγρ. Μήκος`, ty.`Γεωγρ. Πλάτος`, ty.`Ενεργός Από`,
               SUM(pk.`Αγροτικά Συμβόλαια`) + SUM(pk.`Οικιακά Συμβόλαια`) +
               SUM(pk.`Εταιρικά Συμβόλαια`) + SUM(pk.`Βιομηχανικά Συμβόλαια`) AS 'Αριθμός Πελατών'
               FROM `Τοπικός Υποσταθμός` ty
               JOIN `Κατανάλωση Περιοχής` pk ON ty.`ID Υποσταθμού` = pk.`ID Βασικού Υποσταθμού`
               GROUP BY ty.`Όνομα Σταθμού`, `Γεωγρ. Μήκος`, `Γεωγρ. Πλάτος`, `Ενεργός Από`
               ORDER BY `Αριθμός Πελατών` DESC
               LIMIT %s"""
    
    gui.results.place(x=575, y=180)
    gui.results_title.place(x=620, y=120)
    gui.results.configure(font = ("Consolas", 9))
    ExecuteQuery_IntInput(query, gui.input3.get(), gui)
    
    return

def NetworkConnections(gui):
    
    query = """SELECT ty.`Όνομα Σταθμού` AS 'Τοπικός Υποσταθμός', 
        	   s.`Όνομα` AS 'Ενδιάμεσος Σταθμός Μετασχηματισμού',
               dp.`Όνομα Σταθμού` AS 'Σταθμός Παραγωγής'
               FROM `Συνδέεται` s
               JOIN `Τοπικός Υποσταθμός` ty ON ty.`ID Υποσταθμού` = s.`ID Τοπικού Υποσταθμού`
               JOIN `Διεσπαρμένη Παραγωγή` dp ON dp.`ID Μονάδας Παραγωγής` = s.`ID Μονάδας Παραγωγής`
               ORDER BY `Τοπικός Υποσταθμός`, `Ενδιάμεσος Σταθμός Μετασχηματισμού`,
               `Σταθμός Παραγωγής`
               LIMIT %s"""
    
    gui.results.place(x=575, y=180)
    gui.results_title.place(x=575, y=120)
    gui.results.configure(font = ("Consolas", 8))
    ExecuteQuery_IntInput(query, gui.input4.get(), gui)
    
    
    return



def ExecuteQuery_IntInput(query, query_input, gui):
    
    entry = query_input
    if not entry.isdigit():
        gui.results_title.configure(
        text = "Σφάλμα! Δεν πληκτρολογήσατε αριθμό.")
        gui.results.configure(text = "")
    
    else:
        gui.cursor.execute(query, int(entry))
        data=cursor.fetchall()
        df = pd.DataFrame(data)
    
        PrintResults(gui, df)
    
    return


def ExecuteQuery_StrInput(query, query_input, gui):
    entry = query_input
    gui.cursor.execute(query, str(entry))
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    PrintResults(gui, df)
    return


def PrintResults(gui, df):
    
    if(len(df)>0):
        
        gui.results_title.configure(text = "Αποτελέσματα Αναζήτησης:")
        gui.results.configure(text = tabulate(df,headers='keys',tablefmt='psql', showindex=False))
    else:
       gui.results_title.configure(text = "Δεν βρέθηκαν εγγραφές!") 
       gui.results.configure(text = "")
      
    return


if __name__ == '__main__':  

    cursor = ConnectDatabase()
    StartMenu(cursor)
    
    
        
