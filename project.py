# -*- coding: utf-8 -*-

import pymysql as sql
import pymysql.cursors as cur
import pandas as pd
import tkinter as tk

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
        self.window.geometry('1300x650')
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
        self.results = (tk.Label(self.window,  font=("Arial", 10)))
        self.results.place(x=800, y=150)               
    
    #Κουμπιά επιλογής κατηγορίας ερώτησης (στα αριστερά)
        self.btn1 = (tk.Button(self.window, text="Δεδομένα Διεσπαρμένης Παραγωγής", 
        command = lambda: ProductionQueries(self)))
        self.btn1.place(x=50, y=180)
    
        self.btn2 = (tk.Button(self.window, text="Δεδομένα Μέτρησης Παραγωγής", 
        command = lambda: ProductionStatsQueries(self)))
        self.btn2.place(x=50, y=260)
    
        self.btn3 = (tk.Button(self.window, text="Δεδομένα Εταιρειών Παραγωγής", 
        command = lambda: CompaniesQueries(self)))
        self.btn3.place(x=50, y=340)
    
        self.btn4 = (tk.Button(self.window, text="Δεδομένα Κατανάλωσης Περιοχών", 
        command = lambda: AreaQueries(self)))
        self.btn4.place(x=50, y=420)
    
        self.btn5 = (tk.Button(self.window, text="Δεδομένα Μέτρησης Κατανάλωσης", 
        command = lambda: ConsumptionStatsQueries(self)))
        self.btn5.place(x=50, y=500)
    
        self.btn6 = (tk.Button(self.window, text="Δεδομένα Τοπικών Υποσταθμών", 
        command = lambda: SubstationQueries(self)))
        self.btn6.place(x=50, y=580)
    
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
    gui.query1.place(x=350, y=180)
    
    gui.query2.configure(text = "Διεσπαρμένο query 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Διεσπαρμένο query 3")
    gui.query3.place(x=350, y=340)
    
    gui.query4.configure(text = "Διεσπαρμένο query 4")
    gui.query4.place(x=350, y=420)

    gui.query5.configure(text = "Διεσπαρμένο query 5")
    gui.query5.place(x=350, y=500)
    
    return

#Queries Μέτρησης Παραγωγής
def ProductionStatsQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Query μέτρησης παρ. 1")
    gui.query1.place(x=350, y=180)
    
    gui.query2.configure(text = "Query μέτρησης παρ. 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Query μέτρησης παρ. 3")
    gui.query3.place(x=350, y=340)
    
    gui.query4.configure(text = "Query μέτρησης παρ. 4")
    gui.query4.place(x=350, y=420)
    
    gui.query5.configure(text = "Query μέτρησης παρ. 5")
    gui.query5.place(x=350, y=500)
    
    
    return

#Queries Εταιρειών
def CompaniesQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Query εταιρείας 1")
    gui.query1.place(x=350, y=180)
    
    gui.query2.configure(text = "Query εταιρείας 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Query εταιρείας 3")
    gui.query3.place(x=350, y=340)
    
    gui.query4.configure(text = "Query εταιρείας 4")
    gui.query4.place(x=350, y=420)
    
    gui.query5.configure(text = "Query εταιρείας 5")
    gui.query5.place(x=350, y=500)
    
    
    return


#Queries Περιοχών Κατανάλωσης
def AreaQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Περιοχές με τα περισσότερα συμβόλαια")
    gui.query1.place(x=350, y=180)    
    gui.label1.configure(text="Πόλεις εμφάνισης: ")
    gui.label1.place(x=350, y=210)
    gui.input1.insert(10, 10)
    gui.input1.place(x=430, y=210)
    
    gui.query2.configure(text = "Query περιοχής 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Query περιοχής 3")
    gui.query3.place(x=350, y=340)
    
    gui.query4.configure(text = "Query περιοχής 4")
    gui.query4.place(x=350, y=420)
    
    gui.query5.configure(text = "Query περιοχής 5")
    gui.query5.place(x=350, y=500)   
    
    return

#Queries Μέτρησης Παραγωγής
def ConsumptionStatsQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Query μέτρησης κατ. 1")
    gui.query1.place(x=350, y=180)
    
    gui.query2.configure(text = "Query μέτρησης κατ. 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Query μέτρησης κατ. 3")
    gui.query3.place(x=350, y=340)
    
    gui.query4.configure(text = "Query μέτρησης κατ. 4")
    gui.query4.place(x=350, y=420)
    
    gui.query5.configure(text = "Query μέτρησης κατ. 5")
    gui.query5.place(x=350, y=500)
    
    return

#Queries Υπόσταθμων Παραγωγής
def SubstationQueries(gui):
    
    ClearGui(gui)
    
    gui.query1.configure(text = "Query υπάσταθμου 1")
    gui.query1.place(x=350, y=180)
    
    gui.query2.configure(text = "Query υπάσταθμου 2")
    gui.query2.place(x=350, y=260)
    
    gui.query3.configure(text = "Query υπάσταθμου 3")
    gui.query4.place(x=350, y=340)
    
    gui.query4.configure(text = "Query υπάσταθμου 4")
    gui.query4.place(x=350, y=420)
    
    gui.query5.configure(text = "Query υπάσταθμου 5")
    gui.query5.place(x=350, y=500)
    
    return

#Καθαρισμός οθόνης
def ClearGui(gui):
    
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
    
    return


#Όλα τα Queries από εδώ και κάτω
def TestQuery(cursor, results):
    
    query = "SELECT * FROM `Διεσπαρμένη Παραγωγή`"
    cursor.execute(query)
    data=cursor.fetchall()
    df = pd.DataFrame(data)
    results.configure(text = df)
    
    return


if __name__ == '__main__':  

    cursor = ConnectDatabase()
    StartMenu(cursor)
    
    
        
