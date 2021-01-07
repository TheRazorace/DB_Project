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
        self.btn1 = (tk.Button(self.window, text="Δεδομένα Διεσπαρμένης Παραγωγής", 
        command = lambda: ProductionQueries(self)))
        self.btn1.place(x=25, y=180)
    
        self.btn2 = (tk.Button(self.window, text="Δεδομένα Μέτρησης Παραγωγής", 
        command = lambda: ProductionStatsQueries(self)))
        self.btn2.place(x=25, y=260)
    
        self.btn3 = (tk.Button(self.window, text="Δεδομένα Εταιρειών Παραγωγής", 
        command = lambda: CompaniesQueries(self)))
        self.btn3.place(x=25, y=340)
    
        self.btn4 = (tk.Button(self.window, text="Δεδομένα Κατανάλωσης Περιοχών", 
        command = lambda: AreaQueries(self)))
        self.btn4.place(x=25, y=420)
    
        self.btn5 = (tk.Button(self.window, text="Δεδομένα Μέτρησης Κατανάλωσης", 
        command = lambda: ConsumptionStatsQueries(self)))
        self.btn5.place(x=25, y=500)
    
        self.btn6 = (tk.Button(self.window, text="Δεδομένα Τοπικών Υποσταθμών", 
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

#Queries Διεσπαρμένης Παραγωγής
def ProductionQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Αναζήτηση όλων των σταθμών παραγωγής", 
    command = lambda: TestQuery(cursor, gui.results))
    gui.query1.place(x=280, y=180)
    
    gui.query2.configure(text = "Διεσπαρμένο query 2")
    gui.query2.place(x=280, y=260)
    
    gui.query3.configure(text = "Διεσπαρμένο query 3")
    gui.query3.place(x=280, y=340)
    
    gui.query4.configure(text = "Διεσπαρμένο query 4")
    gui.query4.place(x=280, y=420)

    gui.query5.configure(text = "Διεσπαρμένο query 5")
    gui.query5.place(x=280, y=500)
    
    return

#Queries Μέτρησης Παραγωγής
def ProductionStatsQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Παραγωγή Ανά Τέταρτο ",
    command=lambda: Production1(gui))
    gui.query1.place(x=280, y=180)
    
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
    
    # gui.query5.configure(text = "Query εταιρείας 5")
    # gui.query5.place(x=350, y=500)
    
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

## Queries για  πίνακα Μετρήσεις Παραγωγής

def Production1(gui): #Μέγιστη παραγωγή ανά 15 min
    query = "SELECT `Συνολική Μέτρηση (KWh)` , `Όνομα Σταθμού` " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "WHERE `Ώρα` = '2021-01-15 12:00:00' " \
            "GROUP BY `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`" \
            "ORDER BY `Συνολική Μέτρηση (KWh)` DESC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    gui.results_title.configure(text ="Αποτελέσματα")
    gui.results.configure(text = tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
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
    
    
        
