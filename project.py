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

#Ρύθμιση του Gui
def StartMenu(cursor):
    
    #Ορισμός παραθύρου
    window = tk.Tk()
    window.geometry('1300x650')
    window.title("Σύστημα Μεταφοράς Ηλεκτρικής Ενέργειας")
    
    #Τίτλος
    title_lbl = (tk.Label(window,  font=("Arial Bold", 15),
    text="""Επιλέξτε τα δεδομένα που επιθυμείτε να αναζητήσετε! """))
    title_lbl.place(x=420, y=10)  
    
    #Κουμπιά των queries (αυτά που είναι στην μέση)
    query1 = tk.Button(window)   
    query2 = tk.Button(window)
    query3 = tk.Button(window)
    query4 = tk.Button(window)
    query5 = tk.Button(window)
    
    #Πεδίο προβολής απαντήσεων (στα δεξιά)
    results = (tk.Label(window,  font=("Arial", 10)))
    results.place(x=800, y=100)               
    
    #Κουμπιά επιλογής κατηγορίας ερώτησης (στα αριστερά)
    btn1 = (tk.Button(window, text="Δεδομένα Διεσπαρμένης Παραγωγής", 
    command = lambda: ProductionQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn1.place(x=50, y=180)
    
    btn2 = (tk.Button(window, text="Δεδομένα Μέτρησης Παραγωγής", 
    command = lambda: ProductionStatsQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn2.place(x=50, y=260)
    
    btn3 = (tk.Button(window, text="Δεδομένα Εταιρειών Παραγωγής", 
    command = lambda: CompaniesQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn3.place(x=50, y=340)
    
    btn4 = (tk.Button(window, text="Δεδομένα Κατανάλωσης Περιοχών", 
    command = lambda: AreaQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn4.place(x=50, y=420)
    
    btn5 = (tk.Button(window, text="Δεδομένα Μέτρησης Κατανάλωσης", 
    command = lambda: ConsumptionStatsQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn5.place(x=50, y=500)
    
    btn6 = (tk.Button(window, text="Δεδομένα Τοπικών Υποσταθμών", 
    command = lambda: SubstationQueries(cursor, window,
    query1, query2, query3, query4, query5, results)))
    btn6.place(x=50, y=580)
    
    window.mainloop()
    
    
    return

#Κατηγορίες queries
#Κάθε κουμπί στα δεξιά οδηγεί σε μία από τις κατηγορίες των queries
#Σε κάθε query κουμπί ρυθμίζεται εκ νέου το κείμενό του και η συνάρτηση που καλεί

#Queries Διεσπαρμένης Παραγωγής
def ProductionQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Αναζήτηση όλων των σταθμών παραγωγής", 
    command = lambda: TestQuery(cursor, results))
    query1.place(x=350, y=180)
    
    query2.configure(text = "Διεσπαρμένο query 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Διεσπαρμένο query 3", 
    command = lambda: TestQuery(cursor, results))
    query3.place(x=350, y=340)
    
    query4.configure(text = "Διεσπαρμένο query 4", 
    command = lambda: TestQuery(cursor, results))
    query4.place(x=350, y=420)

    query5.configure(text = "Διεσπαρμένο query 5", 
    command = lambda: TestQuery(cursor, results))
    query5.place(x=350, y=500)
    
    return

#Queries Μέτρησης Παραγωγής
def ProductionStatsQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Query μέτρησης παρ. 1")
    query1.place(x=350, y=180)
    
    query2.configure(text = "Query μέτρησης παρ. 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Query μέτρησης παρ. 3")
    query3.place(x=350, y=340)
    
    query4.configure(text = "Query μέτρησης παρ. 4")
    query4.place(x=350, y=420)
    
    query5.configure(text = "Query μέτρησης παρ. 5")
    query5.place(x=350, y=500)
    
    return

#Queries Εταιρειών
def CompaniesQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Query εταιρείας 1")
    query1.place(x=350, y=180)
    
    query2.configure(text = "Query εταιρείας 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Query εταιρείας 3")
    query3.place(x=350, y=340)
    
    query4.configure(text = "Query εταιρείας 4")
    query4.place(x=350, y=420)
    
    query5.configure(text = "Query εταιρείας 5")
    query5.place(x=350, y=500)
    
    return


#Queries Περιοχών Κατανάλωσης
def AreaQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Query περιοχής 1")
    query1.place(x=350, y=180)
    
    query2.configure(text = "Query περιοχής 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Query περιοχής 3")
    query3.place(x=350, y=340)
    
    query4.configure(text = "Query περιοχής 4")
    query4.place(x=350, y=420)
    
    query5.configure(text = "Query περιοχής 5")
    query5.place(x=350, y=500)
    
    return

#Queries Μέτρησης Παραγωγής
def ConsumptionStatsQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Query μέτρησης κατ. 1")
    query1.place(x=350, y=180)
    
    query2.configure(text = "Query μέτρησης κατ. 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Query μέτρησης κατ. 3")
    query3.place(x=350, y=340)
    
    query4.configure(text = "Query μέτρησης κατ. 4")
    query4.place(x=350, y=420)
    
    query5.configure(text = "Query μέτρησης κατ. 5")
    query5.place(x=350, y=500)
    
    return

#Queries Υπόσταθμων Παραγωγής
def SubstationQueries(cursor, window, query1, query2, query3, query4, query5, results):
    
    query1.configure(text = "Query υπάσταθμου 1")
    query1.place(x=350, y=180)
    
    query2.configure(text = "Query υπάσταθμου 2")
    query2.place(x=350, y=260)
    
    query3.configure(text = "Query υπάσταθμου 3")
    query4.place(x=350, y=340)
    
    query4.configure(text = "Query υπάσταθμου 4")
    query4.place(x=350, y=420)
    
    query5.configure(text = "Query υπάσταθμου 5")
    query5.place(x=350, y=500)
    
    return


#Όλα τα Queries
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
    
    
    
    
    
    
    
    
    
