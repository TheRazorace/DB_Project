# -*- coding: utf-8 -*-

import pymysql as sql
import pymysql.cursors as cur
import pandas as pd
import tkinter as tk
from tabulate import tabulate
from textwrap import wrap


# Σύνδεση στην βάση δεδομένων
def ConnectDatabase():
    connection = sql.connect(host="150.140.186.221",
                             port=3306,
                             user="db20_up1047398",
                             password="up1047398",
                             db="project_db20_up1047398",
                             charset="utf8mb4",
                             cursorclass=cur.DictCursor)

    connection.autocommit(True)

    # Δείκτης βάσης
    cursor = connection.cursor()

    return cursor


# Ρύθμιση του Gui με κλάση
class Gui():

    def __init__(self, cursor):
        self.cursor = cursor

        # Ορισμός παραθύρου
        self.window = tk.Tk()
        self.window.geometry('1350x650')
        self.window.title("Σύστημα Μεταφοράς Ηλεκτρικής Ενέργειας")

        # Τίτλος
        self.title_lbl = (tk.Label(self.window, font=("Arial Bold", 15),
                                   text="""Επιλέξτε τα δεδομένα που επιθυμείτε να αναζητήσετε! """))
        self.title_lbl.place(x=420, y=10)

        # Κουμπιά των queries (αυτά που είναι στην μέση)
        self.query1 = tk.Button(self.window)
        self.query2 = tk.Button(self.window)
        self.query3 = tk.Button(self.window)
        self.query4 = tk.Button(self.window)
        self.query5 = tk.Button(self.window)

        # DropDown menus
        # Dates
        options1 = ["2015", "2016", "2017", "2018", "2019", "2020"]
        self.clicked = tk.StringVar()
        self.clicked.set("2015")
        self.dropmn1 = tk.OptionMenu(self.window, self.clicked, *options1)

        # Stations
        self.clicked2 = tk.StringVar()
        self.clicked2.set("Αιολικό Πάρκο Κομποβουνίου Ι")
        self.dropmn2 = tk.OptionMenu(self.window, self.clicked2, *options2)

        # Time

        options3 = ["12:00:00", "12:15:00", "12:30:00", "12:45:00"]
        self.clicked3 = tk.StringVar()
        self.clicked3.set("12:00:00")
        self.dropmn3 = tk.OptionMenu(self.window, self.clicked3, *options3)

        # Εταιρείες ΑΠΕ
        self.clicked4 = tk.StringVar()
        self.clicked4.set("ALEXAKIS ENERGY")
        self.dropmn4 = tk.OptionMenu(self.window, self.clicked4, *options4)

        # Εταιρείες Υποσταθμοι
        self.clicked5 = tk.StringVar()
        self.clicked5.set("ΒΗΜΜΕΠ Α.Β.Ε")
        self.dropmn5 = tk.OptionMenu(self.window, self.clicked5, *options5)

        # Περιοχή
        self.clicked6 = tk.StringVar()
        self.clicked6.set("Αγία Τριάδα")
        self.dropmn6 = tk.OptionMenu(self.window, self.clicked6, *options6)

        # Νομοί
        self.clicked7 = tk.StringVar()
        self.clicked7.set("Αιτωλοακαρνανία")
        self.dropmn7 = tk.OptionMenu(self.window, self.clicked7, *options7)

        # ID Υποσταθμών
        self.clicked8 = tk.StringVar()
        self.clicked8.set("ΤΥ004501")
        self.dropmn8 = tk.OptionMenu(self.window, self.clicked8, *options8)

        # Labels που ίσως χρειαστούν
        self.label1 = tk.Label(self.window, font=("Arial", 7))
        self.label2 = tk.Label(self.window, font=("Arial", 7))
        self.label3 = tk.Label(self.window, font=("Arial", 7))
        self.label4 = tk.Label(self.window, font=("Arial", 7))
        self.label5 = tk.Label(self.window, font=("Arial", 7))
        #       self.labelDelete=tk.Label(self.window, font=("Arial", 7))
        # Inputs που ίσως χρειαστούν
        self.input1 = tk.Entry(self.window, width=20)
        self.input2 = tk.Entry(self.window, width=20)
        self.input3 = tk.Entry(self.window, width=20)
        self.input4 = tk.Entry(self.window, width=20)
        self.input5 = tk.Entry(self.window, width=20)
        #       self.inputDelete=tk.Entry(self.window, width=20)
        # Πεδίο προβολής απαντήσεων (στα δεξιά)
        self.results = (tk.Label(self.window, font=("Consolas", 9),
                                 justify=tk.LEFT, anchor='nw'))
        self.results.place(x=610, y=250)
        self.results_title = tk.Label(self.window, font=("Arial", 12))
        self.results_title.place(x=610, y=120)

        # Κουμπιά μορφοποίησης αποτελεσμάτων
        self.plot_btn = tk.Button(self.window,
                                  text="Προβολή σε γράφημα",
                                  command=lambda: ShowPlot(self.df, self.axis_x, self.axis_y))
        self.csv_btn = tk.Button(self.window,
                                 text="Αποθήκευση σε csv αρχείο",
                                 command=lambda: SaveAsCsv(self.df, self.csv_input.get()))
        self.html_btn = tk.Button(self.window,
                                  text="Αποθήκευση σε html αρχείο",
                                  command=lambda: SaveAsHtml(self.df, self.html_input.get()))

        self.html_lbl = tk.Label(self.window, text="Όνομα φακέλου: ")
        self.csv_lbl = tk.Label(self.window, text="Όνομα φακέλου: ")
        self.html_input = tk.Entry(self.window)
        self.csv_input = tk.Entry(self.window)
        self.html_input.insert(10, "file")
        self.csv_input.insert(10, "file")

        # Κουμπιά επιλογής κατηγορίας ερώτησης (στα αριστερά)
        self.btn1 = (tk.Button(self.window, text="Διεσπαρμένη Παραγωγή",
                               command=lambda: ProductionQueries(self)))
        self.btn1.place(x=25, y=100)

        self.btn2 = (tk.Button(self.window, text="Μετρήσεις Παραγωγής",
                               command=lambda: ProductionStatsQueries(self)))
        self.btn2.place(x=25, y=180)

        self.btn3 = (tk.Button(self.window, text="Εταιρείες Παραγωγής",
                               command=lambda: CompaniesQueries(self)))
        self.btn3.place(x=25, y=260)

        self.btn4 = (tk.Button(self.window, text="Κατανάλωση Περιοχών",
                               command=lambda: AreaQueries(self)))
        self.btn4.place(x=25, y=340)

        self.btn5 = (tk.Button(self.window, text="Μέτρηση Κατανάλωσης",
                               command=lambda: ConsumptionStatsQueries(self)))
        self.btn5.place(x=25, y=420)

        self.btn6 = (tk.Button(self.window, text="Τοπικοί Υποσταθμοί",
                               command=lambda: SubstationQueries(self)))
        self.btn6.place(x=25, y=500)

        self.btn7 = (tk.Button(self.window, text="Εισαγωγή Δεδομένων",
                               command=lambda: InsertQuery(self)))
        self.btn7.place(x=25, y=580)

        self.btn8 = (tk.Button(self.window, text="Διαγραφή Δεδομένων",
                               command=lambda: DeleteQuery(self)))
        self.btn8.place(x=25, y=660)

        # Insert-Set-Delete στοιχεία
        self.isd_lbl1 = tk.Label(self.window)
        self.isd_lbl2 = tk.Label(self.window)
        self.isd_lbl3 = tk.Label(self.window)
        self.isd_lbl4 = tk.Label(self.window)
        self.isd_lbl5 = tk.Label(self.window)
        self.isd_lbl6 = tk.Label(self.window)
        self.isd_lbl7 = tk.Label(self.window)
        self.isd_lbl8 = tk.Label(self.window)
        self.isd_lbl9 = tk.Label(self.window)
        self.isd_lbl10 = tk.Label(self.window)
        self.isd_lbl11 = tk.Label(self.window)
        self.isd_lbl12 = tk.Label(self.window)

        self.isd_input1 = tk.Entry(self.window)
        self.isd_input2 = tk.Entry(self.window)
        self.isd_input3 = tk.Entry(self.window)
        self.isd_input4 = tk.Entry(self.window)
        self.isd_input5 = tk.Entry(self.window)
        self.isd_input6 = tk.Entry(self.window)
        self.isd_input7 = tk.Entry(self.window)
        self.isd_input8 = tk.Entry(self.window)
        self.isd_input9 = tk.Entry(self.window)
        self.isd_input10 = tk.Entry(self.window)
        self.isd_input11 = tk.Entry(self.window)
        self.isd_input12 = tk.Entry(self.window)

        self.exe_btn = tk.Button(self.window, text="Εκτέλεση")
        self.isd_status = tk.Label(self.window)

        # Dataframe δεδομένων
        self.df = pd.DataFrame(None)

        # Plot axises
        self.axis_x = '1'
        self.axis_y = '1'

        self.window.mainloop()


# Εκκίνηση gui με στιγμιότυπο της κλάσης
def StartMenu(cursor):
    gui = Gui(cursor)

    return


# Κατηγορίες queries
# Κάθε κουμπί στα δεξιά οδηγεί σε μία από τις κατηγορίες των queries
# Σε κάθε query κουμπί ρυθμίζεται εκ νέου το κείμενό του και η συνάρτηση που καλεί
# Σε κάθε query κουμπί ρυθμίζεις τι θες να έχουν μέσα τα labels και τα inputs
# με την εντολή configure. Αλλιώς τα κάνεις place_forget() για να μην φαίνονται

# Queries Διεσπαρμένης Παραγωγής
def ProductionQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Σταθμοί παραγωγής Διεσπαρμένης Ενέργειας",
                         command=lambda: Diesp1(gui))
    gui.query1.place(x=280, y=100)

    gui.query2.configure(text="Αρ. Σταθμών ΑΠΕ ανά Νομό",
                         command=lambda: Diesp2(gui))
    gui.query2.place(x=280, y=180)

    gui.query3.configure(text="Είδη Ανανεώσιμης Ενέργειας ανά Νομό",
                         command=lambda: Diesp3(gui))
    gui.query3.place(x=280, y=260)

    gui.query4.configure(text="Ενεργοί Σταθμοί έως:",
                         command=lambda: Diesp4(gui))
    gui.query4.place(x=280, y=340)
    gui.dropmn1.place(x=420, y=340)

    gui.query5.configure(text="Επιλογή Σταθμού",
                         command=lambda: Diesp5(gui))
    gui.query5.place(x=280, y=420)
    gui.dropmn2.place(x=280, y=450)

    return


# Queries Μέτρησης Παραγωγής
def ProductionStatsQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Παραγωγή Ανά Τέταρτο ",
                         command=lambda: Production1(gui))
    gui.query1.place(x=280, y=100)
    gui.dropmn3.place(x=450, y=100)

    gui.query2.configure(text="Συνολική  παραγωγή Σταθμών ανά ώρα ",
                         command=lambda: Production2(gui))
    gui.query2.place(x=280, y=180)

    gui.query3.configure(text="Μέση  παραγωγή ανά 15 min  ανά σταθμό",
                         command=lambda: Production3(gui))
    gui.query3.place(x=280, y=260)

    gui.query4.configure(text="Ποσοστό Προέλευσης Ενέργειας ",
                         command=lambda: Production4(gui))
    gui.query4.place(x=280, y=340)

    gui.query5.configure(text="Παραγωγή στην : ",
                         command=lambda: Production5(gui))
    gui.query5.place(x=280, y=420)
    gui.dropmn7.place(x=280, y=455)
    return


# Queries Εταιρειών
def CompaniesQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Ονόματα και Έδρες Εταιρειών ΑΠΕ ",
                         command=lambda: Etaireia1(gui))
    gui.query1.place(x=280, y=100)

    gui.query2.configure(text="Ταξινόμηση Εταιρειών με βάση τον Αριθμό Έργων ",
                         command=lambda: Etaireia2(gui))
    gui.query2.place(x=280, y=180)

    gui.query3.configure(text="Ταξινόμηση με βαση την Συνολικής Ισχύ σε MW ",
                         command=lambda: Etaireia3(gui))
    gui.query3.place(x=280, y=260)

    gui.query4.configure(text="Εταιρείες με τα 5 μεγαλύτερα έργα ",
                         command=lambda: Etaireia4(gui))
    gui.query4.place(x=280, y=340)

    gui.query5.configure(text="Όνομα Εταιρείας",
                         command=lambda: Etaireia5(gui))
    gui.query5.place(x=280, y=420)
    gui.dropmn4.place(x=400, y=420)

    return


# Queries Περιοχών Κατανάλωσης
def AreaQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Περιοχές βάσει συμβολαίων",
                         command=lambda: AreaAllContracts(gui))
    gui.query1.place(x=280, y=100)
    gui.label1.configure(text="Πλήθος εμφάνισης: ")
    gui.label1.place(x=280, y=130)
    gui.input1.insert(10, 10)
    gui.input1.place(x=370, y=130)

    gui.query2.configure(text="Περιοχές βάσει βιομηχανικών συμβολαίων",
                         command=lambda: AreaIndustrialContracts(gui))
    gui.query2.place(x=280, y=180)
    gui.label2.configure(text="Πλήθος εμφάνισης: ")
    gui.label2.place(x=280, y=210)
    gui.input2.insert(10, 10)
    gui.input2.place(x=370, y=210)

    gui.query3.configure(text="Περιοχές βάσει αγροτικών συμβολαίων",
                         command=lambda: AreaAgriContracts(gui))
    gui.query3.place(x=280, y=260)
    gui.label3.configure(text="Πλήθος εμφάνισης: ")
    gui.label3.place(x=280, y=290)
    gui.input3.insert(10, 10)
    gui.input3.place(x=370, y=290)

    gui.query4.configure(text="Τοπικός υποσταθμός περιοχής",
                         command=lambda: AreaStation(gui))
    gui.query4.place(x=280, y=340)
    gui.dropmn6.place(x=280, y=370)

    # gui.label4.configure(text="Περιοχή αναζήτησης: ")
    # gui.label4.place(x=280, y=370)
    # gui.input4.insert(10, 'Πάτρα - Κέντρο')
    # gui.input4.place(x=375, y=370)

    # gui.query5.configure(text = "Query περιοχής 5")
    # gui.query5.place(x=350, y=500)

    return


# Queries Μέτρησης Κατανάλωσης
def ConsumptionStatsQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Κατανάλωση ανά 15 λεπτά",
                         command=lambda: Consumption15min(gui))
    gui.query1.place(x=280, y=100)
    gui.label1.configure(text="Πλήθος εμφάνισης: ")
    gui.label1.place(x=280, y=130)
    gui.input1.insert(10, 10)
    gui.input1.place(x=370, y=130)

    gui.query2.configure(text="Κατανάλωση σε 1 ώρα",
                         command=lambda: Consumption1Hr(gui))
    gui.query2.place(x=280, y=180)
    gui.label2.configure(text="Πλήθος εμφάνισης: ")
    gui.label2.place(x=280, y=210)
    gui.input2.insert(10, 10)
    gui.input2.place(x=370, y=210)
    gui.query2.place(x=280, y=180)

    gui.query3.configure(text="Κατανάλωση σε 1 ώρα ανά νομό",
                         command=lambda: CountyConsumption1Hr(gui))
    gui.query3.place(x=280, y=260)

    gui.query4.configure(text="Ποσοστό 'πράσινης' κατνάλωσης",
                         command=lambda: GreenConsumption(gui))
    gui.query4.place(x=280, y=340)

    # gui.query5.configure(text = "Query μέτρησης κατ. 5")
    # gui.query5.place(x=280, y=420)

    return


# Queries Υπόσταθμων Παραγωγής
def SubstationQueries(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Σταθμοί χαμηλής τάσης",
                         command=lambda: CommonStations(gui))
    gui.query1.place(x=280, y=100)
    gui.label1.configure(text="Πλήθος εμφάνισης: ")
    gui.label1.place(x=280, y=130)
    gui.input1.insert(10, 10)
    gui.input1.place(x=370, y=130)

    gui.query2.configure(text="Σταθμοί εργοστασιακής χρήσης",
                         command=lambda: IndustrialStations(gui))
    gui.query2.place(x=280, y=180)
    gui.label2.configure(text="Πλήθος εμφάνισης: ")
    gui.label2.place(x=280, y=210)
    gui.input2.insert(10, 10)
    gui.input2.place(x=370, y=210)

    gui.query3.configure(text="Πλήθος πελατών εξυπηρέτησης σταθμών",
                         command=lambda: StationsSort(gui))
    gui.query3.place(x=280, y=260)
    gui.label3.configure(text="Πλήθος εμφάνισης: ")
    gui.label3.place(x=280, y=290)
    gui.input3.insert(10, 10)
    gui.input3.place(x=370, y=290)

    gui.query4.configure(text="Στοιχεία σύνδεσης σταθμών",
                         command=lambda: NetworkConnections(gui))
    gui.query4.place(x=280, y=340)
    gui.label4.configure(text="Επιλογή Σταθμού: ")
    gui.label4.place(x=280, y=370)
    gui.dropmn5.place(x=370, y=370)
    # gui.input4.insert(10, 10)
    # gui.input4.place(x=370, y=370)

    # gui.query5.configure(text = "Query υπάσταθμου 5")
    # gui.query5.place(x=350, y=500)

    return


# Insert Queries
def InsertQuery(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Προσθήκη Σταθμού Παραγωγής",
                         command=lambda: InsertDiesp(gui))
    gui.query1.place(x=280, y=100)

    gui.query2.configure(text="Προσθήκη Τοπικού Υποσταθμού",
                         command=lambda: InsertSubstation(gui))
    gui.query2.place(x=280, y=180)

    gui.query3.configure(text="Προσθήκη Περιοχής",
                         command=lambda: InsertArea(gui))
    gui.query3.place(x=280, y=260)

    gui.query4.configure(text="Προσθήκη Εταιρείας",
                         command=lambda: InsertCompany(gui))
    gui.query4.place(x=280, y=340)

    return


# Delete Queries
def DeleteQuery(gui):
    ClearCentralGui(gui)

    gui.query1.configure(text="Διαγραφή Σταθμού Παραγωγής",
                         command=lambda: delete_diesp(gui))
    gui.query1.place(x=280, y=100)
    gui.dropmn2.place(x=280, y=130)

    gui.query2.configure(text="Διαγραφή Τοπικού Υποσταθμού",
                         command=lambda: delete_ypo(gui))
    gui.query2.place(x=280, y=180)
    gui.dropmn5.place(x=280, y=210)

    gui.query3.configure(text="Διαγραφή Περιοχής",
                         command=lambda: delete_area(gui))
    gui.query3.place(x=280, y=260)
    gui.dropmn6.place(x=280, y=300)

    ##    gui.labelDelete.configure(text="T.K.: ")
    ##    gui.labelDelete.place(x=400, y=305)
    ##    gui.inputDelete.insert(10, 10)
    ##   gui.inputDelete.place(x=430, y=305)

    gui.query4.configure(text="Διαγραφή Εταιρείας",
                         command=lambda: delete_etairia(gui))
    gui.query4.place(x=280, y=340)
    gui.dropmn4.place(x=280, y=370)

    return


# Καθαρισμός οθόνης
def ClearCentralGui(gui):
    # Κρύψιμο των κουμπιών
    gui.query1.place_forget()
    gui.query2.place_forget()
    gui.query3.place_forget()
    gui.query4.place_forget()
    gui.query5.place_forget()

    # Κρύψιμο των labels από άλλα κουμπιά
    gui.label1.place_forget()
    gui.label2.place_forget()
    gui.label3.place_forget()
    gui.label4.place_forget()
    gui.label5.place_forget()
    #    gui.labelDelete.place_forget()

    # Κρύψιμο των Drop Menus
    gui.dropmn1.place_forget()
    gui.dropmn2.place_forget()
    gui.dropmn3.place_forget()
    gui.dropmn4.place_forget()
    gui.dropmn5.place_forget()
    gui.dropmn6.place_forget()
    gui.dropmn7.place_forget()

    # Κρύψιμο των inputs από άλλα κουμπιά
    gui.input1.place_forget()
    gui.input2.place_forget()
    gui.input3.place_forget()
    gui.input4.place_forget()
    gui.input5.place_forget()
    #    gui.inputDelete.place_forget()

    # Διαγραφή περιεχομένου των inputs
    gui.input1.delete(0, tk.END)
    gui.input2.delete(0, tk.END)
    gui.input3.delete(0, tk.END)
    gui.input4.delete(0, tk.END)
    gui.input5.delete(0, tk.END)
    #    gui.inputDelete.delete(0, tk.END)
    # Τα κουμπιά να μη δείχνουν σε κάποια συνάρτηση
    gui.query1.configure(command=lambda: None)
    gui.query2.configure(command=lambda: None)
    gui.query3.configure(command=lambda: None)
    gui.query4.configure(command=lambda: None)
    gui.query5.configure(command=lambda: None)

    # Κρύψιμο αποτελεσμάτων
    gui.results.configure(text="")
    gui.results_title.configure(text="")
    gui.results.configure(font=("Consolas", 9))
    gui.results.place(x=610, y=250)

    # Κρύψιμο στοιχείων χειρισμού αποτελεσμάτων
    gui.csv_btn.place_forget()
    gui.html_btn.place_forget()
    gui.plot_btn.place_forget()
    gui.csv_lbl.place_forget()
    gui.html_lbl.place_forget()
    gui.csv_input.place_forget()
    gui.html_input.place_forget()

    ClearRightGui(gui)

    return


def ClearRightGui(gui):
    gui.isd_lbl1.place_forget()
    gui.isd_lbl2.place_forget()
    gui.isd_lbl3.place_forget()
    gui.isd_lbl4.place_forget()
    gui.isd_lbl5.place_forget()
    gui.isd_lbl6.place_forget()
    gui.isd_lbl7.place_forget()
    gui.isd_lbl8.place_forget()
    gui.isd_lbl9.place_forget()
    gui.isd_lbl10.place_forget()
    gui.isd_lbl11.place_forget()
    gui.isd_lbl12.place_forget()

    gui.dropmn2.place_forget()
    gui.dropmn8.place_forget()

    gui.isd_input1.place_forget()
    gui.isd_input2.place_forget()
    gui.isd_input3.place_forget()
    gui.isd_input4.place_forget()
    gui.isd_input5.place_forget()
    gui.isd_input6.place_forget()
    gui.isd_input7.place_forget()
    gui.isd_input8.place_forget()
    gui.isd_input9.place_forget()
    gui.isd_input10.place_forget()
    gui.isd_input11.place_forget()
    gui.isd_input12.place_forget()

    gui.isd_input1.delete(0, tk.END)
    gui.isd_input2.delete(0, tk.END)
    gui.isd_input3.delete(0, tk.END)
    gui.isd_input4.delete(0, tk.END)
    gui.isd_input5.delete(0, tk.END)
    gui.isd_input6.delete(0, tk.END)
    gui.isd_input7.delete(0, tk.END)
    gui.isd_input8.delete(0, tk.END)
    gui.isd_input9.delete(0, tk.END)
    gui.isd_input10.delete(0, tk.END)
    gui.isd_input11.delete(0, tk.END)
    gui.isd_input12.delete(0, tk.END)

    gui.exe_btn.place_forget()
    gui.isd_status.place_forget()

    return


## Queries για  πίνακα Διεσπαρμένη Ενέργεια

def Diesp1(gui):  # Προβολή Σταθμών ανά Νομό με φθίνοντα αριθμό Ισχύος
    query = "SELECT `Νομός`, `Όνομα Σταθμού`  , `Εγκατεστημένη Ισχύς (MW)` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "ORDER BY `Νομός` ASC ,`Όνομα Σταθμού`  ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    PlaceFileButtons(gui)

    return


def Diesp2(gui):  # Αριθμός Σταθμών ΑΠΕ ανά Νομό
    query = "SELECT `Νομός`, COUNT(`ID Μονάδας Παραγωγής`) as `Αρ. Μονάδσων Διεσπαρμένης Παραγωγής` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "GROUP BY `Νομός` " \
            "ORDER BY `Αρ. Μονάδσων Διεσπαρμένης Παραγωγής` DESC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    PlaceFileButtons(gui)

    return


def Diesp3(gui):  # Αριθμός Σταθμών ΑΠΕ ανά Νομό
    query = "SELECT  COUNT(`Ενέργεια`) as `Αριθμός Μονάδων` ,`Ενέργεια` ,`Νομός`  " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "GROUP BY `Ενέργεια` , `Νομός` " \
            "ORDER BY `Νομός` ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    PlaceFileButtons(gui)

    return


def Diesp4(gui):
    query = "SELECT   `Όνομα Σταθμού` ,`Ενέργεια` ,`Νομός` ,`Εγκατεστημένη Ισχύς (MW)` " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "WHERE   YEAR(`Ενεργός Από:`) <= %s  " \
            "ORDER BY `Νομός` ASC  "

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.clicked.get(), gui)


def Diesp5(gui):  # Πληροφορίες Σταθμού
    query = "SELECT `Όνομα Σταθμού`,`Εγκατεστημένη Ισχύς (MW)`,`Ενέργεια`,`Νομός` , `Ενεργός Από:`  " \
            "FROM `Διεσπαρμένη Παραγωγή` " \
            "WHERE `Όνομα Σταθμού` = %s  "
    PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked2.get(), gui)
    return


def delete_diesp(gui):
    query = "SELECT `Όνομα Σταθμού` FROM `Διεσπαρμένη Παραγωγή` " \
            "WHERE `Όνομα Σταθμού`=%s "
    ##PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked2.get(), gui)
    gui.isd_status.configure(text="Η Διαγραφή έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)


## Queries για  πίνακα Εταιρείες

def Etaireia1(gui):  # Προβολή στοιχείων εταιρείας
    query = "SELECT DISTINCT  `Όνομα Εταιρείας` , `Έδρα Εταιρείας` " \
            "FROM `Εταιρεία` " \
            "ORDER BY `Έδρα Εταιρείας` ,`Όνομα Εταιρείας`  ASC  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))

    return


def Etaireia2(gui):  # Ταξινόμηση εταιρειών με βάση τον αριθμό έργων
    query = "SELECT `Όνομα Εταιρείας` ,COUNT('ID Διεσπαρμένης Παραγωγής')  as `Αριθμός Έργων` " \
            "FROM `Εταιρεία`" \
            "GROUP  BY `Όνομα Εταιρείας` " \
            "ORDER BY `Αριθμός Έργων` DESC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Αριθμός Έργων'
    gui.axis_x = 'Όνομα Εταιρείας'

    return


def Etaireia3(gui):  # Ταξινόμηση εταιρειών με βάση τα συνολικά έργα
    query = "SELECT `Όνομα Εταιρείας`  ,SUM(`Εγκατεστημένη Ισχύς (MW)`) as `Συνολική Ισχύς Έργων`  " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "GROUP BY `Όνομα Εταιρείας`" \
            "ORDER BY `Συνολική Ισχύς Έργων` DESC , `Όνομα Εταιρείας`   "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Συνολική Ισχύς Έργων'
    gui.axis_x = 'Όνομα Εταιρείας'

    return


def Etaireia4(gui):  # Ταξινόμηση ανα έργο ίσως και ανα περιοχή ??
    query = "SELECT `Όνομα Εταιρείας` , `Εγκατεστημένη Ισχύς (MW)` , `Ενέργεια` " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "ORDER BY `Εγκατεστημένη Ισχύς (MW)` DESC , `Όνομα Εταιρείας` " \
            "LIMIT 5  "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Εγκατεστημένη Ισχύς (MW)'
    gui.axis_x = 'Όνομα Εταιρείας'

    return


def Etaireia5(gui):  # Ταξινόμηση ανα έργο ίσως και ανα περιοχή ??
    query = "SELECT `Όνομα Σταθμού`,`Εγκατεστημένη Ισχύς (MW)` , `Ενέργεια` , `Νομός` " \
            "FROM `Εταιρεία` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `ID Διεσπαρμένης Παραγωγής`= `ID Μονάδας Παραγωγής`" \
            "WHERE `Όνομα Εταιρείας`=%s " \
            "ORDER BY `Εγκατεστημένη Ισχύς (MW)` DESC  " \
            "LIMIT 5  "

    PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked4.get(), gui)

    return


def delete_etairia(gui):  # Ταξινόμηση ανα έργο ίσως και ανα περιοχή ??
    query = "SELECT `Όνομα Εταιρείας` FROM `Εταιρεία` " \
            "WHERE `Εταιρεία`.`Όνομα Εταιρείας`=%s "
    ExecuteQuery_StrInput(query, gui.clicked4.get(), gui)
    gui.isd_status.configure(text="Η Διαγραφή έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)


## Queries για  πίνακα Μετρήσεις Παραγωγής

def Production1(gui):  # Μέγιστη παραγωγή ανά 15 min
    query = "SELECT `Συνολική Μέτρηση (KWh)` , `Όνομα Σταθμού` " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "WHERE TIME(`Ώρα`) = %s " \
            "ORDER BY `Συνολική Μέτρηση (KWh)` DESC "

    PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked3.get(), gui)

    return


def Production2(gui):  # Συνολική  παραγωγή ανά 1 hour  ανά σταθμό
    query = "SELECT SUM(`Συνολική Μέτρηση (KWh)`) as  `Συνολική Παραγωγή (KW)`,`Διεσπαρμένη Παραγωγή`.`Όνομα Σταθμού`  " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`" \
            "ORDER BY `Συνολική Παραγωγή (KW)` DESC "

    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))

    return


def Production3(gui):  # Μέση  παραγωγή ανά 15 min  ανά σταθμό
    query = "SELECT AVG(`Συνολική Μέτρηση (KWh)`) as  `Μέση Παραγωγή (KW) / 15 min`,`Διεσπαρμένη Παραγωγή`.`Όνομα Σταθμού`  " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`" \
            "ORDER BY `Μέση Παραγωγή (KW) / 15 min` DESC "

    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))

    return


def Production4(gui):  # Ποσοστό Προέλευσης Ενέργειας
    query = "SELECT SUM(`Συνολική Μέτρηση (KWh)`)/(SELECT SUM(`Μέτρηση Παραγωγής`.`Συνολική Μέτρηση (KWh)`) FROM `Μέτρηση Παραγωγής` )*100 as `Ποσοστό Συνολικής Παραγωγής %`" \
            ",`Διεσπαρμένη Παραγωγή`.`Ενέργεια`  as `Είδος Ενέργειας` " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή`" \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "GROUP BY `Διεσπαρμένη Παραγωγή`.`Ενέργεια`" \
            "ORDER BY `Διεσπαρμένη Παραγωγή`.`Ενέργεια` ASC "
    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Ποσοστό Συνολικής Παραγωγής'
    gui.axis_x = 'Είδος Ενέργειας'

    return


def Production5(gui):
    query = "SELECT SUM(`Μέτρηση Παραγωγής`.`Συνολική Μέτρηση (KWh)`) as `Παραγώμενη Ενέργεια (KW)` ,`Διεσπαρμένη Παραγωγή`.`Ενέργεια`" \
            ", SUM(`Μέτρηση Παραγωγής`.`Συνολική Μέτρηση (KWh)`)/ (SELECT  SUM(`Μέτρηση Παραγωγής`.`Συνολική Μέτρηση (KWh)`) "\
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή` "\
            "ON `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`=`Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`"\
            "WHERE `Διεσπαρμένη Παραγωγή`.`Νομός`= %s )*100 as `Ποσοστό`   " \
            "FROM `Μέτρηση Παραγωγής` JOIN `Διεσπαρμένη Παραγωγή` " \
            "on `Μέτρηση Παραγωγής`.`ID Μονάδας Παραγωγής`= `Διεσπαρμένη Παραγωγή`.`ID Μονάδας Παραγωγής`" \
            "WHERE `Διεσπαρμένη Παραγωγή`.`Νομός` =  %s " \
            "GROUP BY `Διεσπαρμένη Παραγωγή`.`Ενέργεια` " \
            "ORDER BY `Παραγώμενη Ενέργεια (KW)` DESC"

    # ExecuteQuery_StrInput(query, gui.clicked7.get(), gui)
    gui.cursor.execute(query, (gui.clicked7.get(),gui.clicked7.get()))
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Παραγώμενη Ενέργεια (KW)'
    gui.axis_x = 'Ενέργεια'


# Queries Κατανάλωσης Περιοχής
def AreaAllContracts(gui):
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`,
            SUM(`Οικιακά Συμβόλαια`) + SUM(`Εταιρικά Συμβόλαια`) + 
            SUM(`Βιομηχανικά Συμβόλαια`) + SUM(`Αγροτικά Συμβόλαια`) AS `Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Συμβόλαια` DESC
            LIMIT %s """

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input1.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Συμβόλαια'
    gui.df[gui.axis_y] = [int(x) for x in gui.df[gui.axis_y]]
    gui.axis_x = 'Περιοχή'

    return


def AreaIndustrialContracts(gui):
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`, `Βιομηχανικά Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Βιομηχανικά Συμβόλαια` DESC
            LIMIT %s"""

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input2.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Βιομηχανικά Συμβόλαια'
    gui.axis_x = 'Περιοχή'

    return


def AreaAgriContracts(gui):
    query = """SELECT `Περιοχή`,`Τ.Κ.`,`Νομός`,`Διαμέρισμα`, `Αγροτικά Συμβόλαια`
            FROM `Κατανάλωση Περιοχής`
            GROUP BY `Περιοχή`
            ORDER BY `Αγροτικά Συμβόλαια` DESC
            LIMIT %s"""

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input3.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Αγροτικά Συμβόλαια'
    gui.axis_x = 'Περιοχή'

    return


def AreaStation(gui):
    query = """SELECT kp.`Περιοχή`,kp.`Τ.Κ.`, ty.`Όνομα Σταθμού` AS `Βασικός Υποσταθμός Περιοχής` 
            FROM `Κατανάλωση Περιοχής` kp 
            JOIN `Τοπικός Υποσταθμός` ty ON kp.`ID Βασικού Υποσταθμού` = ty.`ID Υποσταθμού`
            WHERE `Περιοχή` = %s"""

    gui.cursor.execute(query, gui.clicked6.get())
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    PlaceFileButtons(gui)
    PrintResults(gui, df)

    return


def delete_area(gui):
    query = "SELECT `Περιοχή`  FROM `Κατανάλωση Περιοχής` " \
            "WHERE `Κατανάλωση Περιοχής`.`Περιοχή`=%s "
    ##PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked6.get(), gui)
    gui.isd_status.configure(text="Η Διαγραφή έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)


# Queries Τοπικού Υποσταθμού
def CommonStations(gui):
    query = """SELECT `Όνομα Σταθμού`,`Γεωγρ. Μήκος`,`Γεωγρ. Πλάτος`,`Ενεργός Από` 
            FROM `Τοπικός Υποσταθμός` 
            WHERE `Μετασχηματισμός Τάσης` = '20KV/400V'
            LIMIT %s"""

    gui.results.place(x=610, y=250)
    gui.results.configure(font=("Consolas", 10))
    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input1.get(), gui)

    return


def IndustrialStations(gui):
    query = """SELECT `Όνομα Σταθμού`,`Γεωγρ. Μήκος`,`Γεωγρ. Πλάτος`,`Ενεργός Από` 
            FROM `Τοπικός Υποσταθμός` 
            WHERE `Μετασχηματισμός Τάσης` != '20KV/400V'
            LIMIT %s"""

    gui.results.place(x=610, y=250)
    gui.results.configure(font=("Consolas", 10))
    PlaceFileButtons(gui)
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

    gui.results.place(x=575, y=250)
    gui.results.configure(font=("Consolas", 9))
    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input3.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Αριθμός Πελατών'
    gui.df[gui.axis_y] = [int(x) for x in gui.df[gui.axis_y]]
    gui.axis_x = 'Όνομα Σταθμού'

    return


def NetworkConnections(gui):
    query = """SELECT ty.`Όνομα Σταθμού` AS 'Τοπικός Υποσταθμός', 
        	   s.`Όνομα` AS 'Ενδιάμεσος Σταθμός Μετασχηματισμού',
               dp.`Όνομα Σταθμού` AS 'Σταθμός Παραγωγής'
               FROM `Συνδέεται` s
               JOIN `Τοπικός Υποσταθμός` ty ON ty.`ID Υποσταθμού` = s.`ID Τοπικού Υποσταθμού`
               JOIN `Διεσπαρμένη Παραγωγή` dp ON dp.`ID Μονάδας Παραγωγής` = s.`ID Μονάδας Παραγωγής`
              WHERE ty.`Όνομα Σταθμού`= %s
               ORDER BY `Τοπικός Υποσταθμός`, `Ενδιάμεσος Σταθμός Μετασχηματισμού` """

    gui.results.place(x=575, y=250)
    gui.results.configure(font=("Consolas", 8))
    PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked5.get(), gui)

    return


def delete_ypo(gui):
    query = "SELECT `Τοπικός Υποσταθμός`.`Όνομα Σταθμού`  FROM `Τοπικός Υποσταθμός` " \
            "WHERE `Τοπικός Υποσταθμός`.`Όνομα Σταθμού`=%s "
    ##PlaceFileButtons(gui)
    ExecuteQuery_StrInput(query, gui.clicked5.get(), gui)
    gui.isd_status.configure(text="Η Διαγραφή έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)
    return


# Queries Μέτρησης Κατανάλωσης
def Consumption1Hr(gui):
    query = """SELECT `Περιοχή`, 
               SUM(`Συνολική Κατανάλωση (KWh)`) AS 'Κατανάλωση σε 1 ώρα'
               FROM `Μέτρηση Κατανάλωσης` 
               GROUP BY `Περιοχή`
               ORDER BY `Κατανάλωση σε 1 ώρα` DESC
               LIMIT %s"""

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input2.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Κατανάλωση σε 1 ώρα'
    gui.axis_x = 'Περιοχή'

    return


def Consumption15min(gui):
    query = """SELECT `Περιοχή`, 
               AVG(`Συνολική Κατανάλωση (KWh)`) AS 'Μέση Κατανάλωση ανά 15 λεπτά'
               FROM `Μέτρηση Κατανάλωσης` 
               GROUP BY `Περιοχή`
               ORDER BY `Μέση Κατανάλωση ανά 15 λεπτά`
               LIMIT %s"""

    PlaceFileButtons(gui)
    ExecuteQuery_IntInput(query, gui.input1.get(), gui)
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Μέση Κατανάλωση ανά 15 λεπτά'
    gui.axis_x = 'Περιοχή'

    return


def CountyConsumption1Hr(gui):
    query = """SELECT kp.`Νομός`, 
            SUM(mk.`Συνολική Κατανάλωση (KWh)`) AS 'Κατανάλωση σε 1 ώρα'
            FROM `Μέτρηση Κατανάλωσης` mk
            NATURAL JOIN `Κατανάλωση Περιοχής` kp
            GROUP BY kp.`Νομός`
            ORDER BY kp.`Νομός`"""

    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης:")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Κατανάλωση σε 1 ώρα'
    gui.axis_x = 'Νομός'

    return


def GreenConsumption(gui):
    query = """SELECT kp.`Νομός` AS 'Νομός', 
            SUM(mk.`Συνολική Κατανάλωση (KWh)`) AS 'Κατανάλωση σε 1 ώρα',
            SUM(mp.`Συνολική Μέτρηση (KWh)`) AS 'Παραγωγή σε 1 ώρα',
            (SUM(mp.`Συνολική Μέτρηση (KWh)`)/SUM(mk.`Συνολική Κατανάλωση (KWh)`))*100
            AS 'Ποσοστό Πράσινης Κατανάλωσης'
            FROM `Μέτρηση Κατανάλωσης` mk
            NATURAL JOIN `Κατανάλωση Περιοχής` kp
            NATURAL JOIN `Διεσπαρμένη Παραγωγή` dp
            NATURAL JOIN `Μέτρηση Παραγωγής` mp
            GROUP BY `Νομός`
            ORDER BY `Νομός`"""

    gui.cursor.execute(query)
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    gui.results_title.configure(text="Αποτελέσματα Αναζήτησης:")
    PlaceFileButtons(gui)
    gui.results.configure(text=tabulate(gui.df, headers='keys', tablefmt='psql', showindex=False))
    gui.plot_btn.place(x=1010, y=150)
    gui.axis_y = 'Ποσοστό Πράσινης Κατανάλωσης'
    gui.axis_x = 'Νομός'

    return


def ExecuteQuery_IntInput(query, query_input, gui):
    entry = query_input
    if not entry.isdigit():
        gui.results_title.configure(
            text="Σφάλμα! Δεν πληκτρολογήσατε αριθμό.")
        gui.results.configure(text="")

    else:
        gui.cursor.execute(query, int(entry))
        data = cursor.fetchall()
        gui.df = pd.DataFrame(data)

        PrintResults(gui, gui.df)

    return


def ExecuteQuery_StrInput(query, query_input, gui):
    entry = query_input
    gui.cursor.execute(query, str(entry))
    data = cursor.fetchall()
    gui.df = pd.DataFrame(data)
    PrintResults(gui, gui.df)
    return


def PrintResults(gui, df):
    if (len(df) > 0):
        gui.results_title.configure(text="Αποτελέσματα Αναζήτησης: ")
        gui.results.configure(text=tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    else:
        gui.results_title.configure(text="Δεν βρέθηκαν εγγραφές!")
        gui.results.configure(text="")

    return


def ShowPlot(df, axis_x, axis_y):
    df[axis_x] = ['\n'.join(wrap(x, 12)) for x in df[axis_x]]
    df.plot.bar(x=axis_x, y=axis_y, rot=0, figsize=(15, 10), fontsize=10)

    return


def SaveAsCsv(df, filename):
    compression_opts = dict(method='zip', archive_name=filename + '.csv')
    df.to_csv(filename + '.zip', index=False,
              compression=compression_opts, encoding='utf-8-sig')

    return


def SaveAsHtml(df, filename):
    html = df.to_html()
    text_file = open(filename, "w")
    text_file.write(html)
    text_file.close()

    return


def PlaceFileButtons(gui):
    gui.csv_btn.place(x=610, y=150)
    gui.csv_lbl.place(x=610, y=177)
    gui.csv_input.place(x=610, y=197)

    gui.html_btn.place(x=810, y=150)
    gui.html_lbl.place(x=810, y=177)
    gui.html_input.place(x=810, y=197)

    gui.plot_btn.place_forget()

    return


def InsertDiesp(gui):
    ClearRightGui(gui)

    gui.results_title.configure(text="Δεδομένα εισαγωγής:")

    gui.isd_lbl1.configure(text="ID: ")
    gui.isd_lbl1.place(x=640, y=160)
    gui.isd_input1.place(x=700, y=160)

    gui.isd_lbl2.configure(text="Όνομα: ")
    gui.isd_lbl2.place(x=940, y=160)
    gui.isd_input2.place(x=1000, y=160)

    gui.isd_lbl3.configure(text="Ισχύς (MW): ")
    gui.isd_lbl3.place(x=640, y=220)
    gui.isd_input3.place(x=720, y=220)

    gui.isd_lbl4.configure(text="Μορφή Ενέργειας: ")
    gui.isd_lbl4.place(x=940, y=220)
    gui.isd_input4.place(x=1050, y=220)

    gui.isd_lbl5.configure(text="Ενέργεια: ")
    gui.isd_lbl5.place(x=640, y=280)
    gui.isd_input5.place(x=700, y=280)

    gui.isd_lbl6.configure(text="Τεχνολογία: ")
    gui.isd_lbl6.place(x=940, y=280)
    gui.isd_input6.place(x=1040, y=280)

    gui.isd_lbl7.configure(text="Γεωγρ. Μήκος: ")
    gui.isd_lbl7.place(x=640, y=340)
    gui.isd_input7.place(x=740, y=340)

    gui.isd_lbl8.configure(text="Γεωγρ. Πλάτος: ")
    gui.isd_lbl8.place(x=940, y=340)
    gui.isd_input8.place(x=1040, y=340)

    gui.isd_lbl9.configure(text="Διαμέρισμα: ")
    gui.isd_lbl9.place(x=940, y=400)
    gui.isd_input9.place(x=1040, y=400)

    gui.isd_lbl10.configure(text="Νομός: ")
    gui.isd_lbl10.place(x=640, y=400)
    gui.isd_input10.place(x=700, y=400)

    gui.isd_lbl11.configure(text="Ενεργός από: ")
    gui.isd_lbl11.place(x=640, y=460)
    gui.isd_input11.place(x=740, y=460)

    gui.isd_lbl12.configure(text="Τάση: ")
    gui.isd_lbl12.place(x=940, y=460)
    gui.isd_input12.place(x=1040, y=460)

    gui.exe_btn.place(x=640, y=560)
    gui.exe_btn.configure(command=lambda: ExeInsertDiesp(gui))

    return


def InsertSubstation(gui):
    ClearRightGui(gui)

    gui.results_title.configure(text="Δεδομένα εισαγωγής:")

    gui.isd_lbl1.configure(text="ID: ")
    gui.isd_lbl1.place(x=640, y=160)
    gui.isd_input1.place(x=700, y=160)

    gui.isd_lbl2.configure(text="Όνομα: ")
    gui.isd_lbl2.place(x=940, y=160)
    gui.isd_input2.place(x=1000, y=160)

    gui.isd_lbl3.configure(text="Γεωγρ. Μήκος: ")
    gui.isd_lbl3.place(x=640, y=220)
    gui.isd_input3.place(x=740, y=220)

    gui.isd_lbl4.configure(text="Γεωγρ. Πλάτος: ")
    gui.isd_lbl4.place(x=940, y=220)
    gui.isd_input4.place(x=1040, y=220)

    gui.isd_lbl5.configure(text="Διαμέρισμα: ")
    gui.isd_lbl5.place(x=640, y=280)
    gui.isd_input5.place(x=740, y=280)

    gui.isd_lbl6.configure(text="Νομός: ")
    gui.isd_lbl6.place(x=940, y=280)
    gui.isd_input6.place(x=1000, y=280)

    gui.isd_lbl7.configure(text="Μετασχ. Τάσης: ")
    gui.isd_lbl7.place(x=640, y=340)
    gui.isd_input7.place(x=740, y=340)

    gui.isd_lbl8.configure(text="Ενεργός Από: ")
    gui.isd_lbl8.place(x=940, y=340)
    gui.isd_input8.place(x=1040, y=340)

    gui.isd_lbl9.configure(text="Συχνότητα: ")
    gui.isd_lbl9.place(x=640, y=400)
    gui.isd_input9.place(x=740, y=400)

    gui.exe_btn.place(x=640, y=460)
    gui.exe_btn.configure(command=lambda: ExeInsertSubstation(gui))

    return


def InsertArea(gui):
    ClearRightGui(gui)

    gui.results_title.configure(text="Δεδομένα εισαγωγής:")

    gui.isd_lbl1.configure(text="Περιοχή: ")
    gui.isd_lbl1.place(x=640, y=160)
    gui.isd_input1.place(x=700, y=160)

    gui.isd_lbl2.configure(text="Τ.Κ.: ")
    gui.isd_lbl2.place(x=940, y=160)
    gui.isd_input2.place(x=1000, y=160)

    gui.isd_lbl3.configure(text="Νομός: ")
    gui.isd_lbl3.place(x=640, y=220)
    gui.isd_input3.place(x=710, y=220)

    gui.isd_lbl4.configure(text="Διαμέρισμα: ")
    gui.isd_lbl4.place(x=940, y=220)
    gui.isd_input4.place(x=1020, y=220)

    gui.isd_lbl5.configure(text="Οικιακά Συμβόλαια: ")
    gui.isd_lbl5.place(x=640, y=280)
    gui.isd_input5.place(x=750, y=280)

    gui.isd_lbl6.configure(text="Εταιρικά Συμβόλαια: ")
    gui.isd_lbl6.place(x=940, y=280)
    gui.isd_input6.place(x=1060, y=280)

    gui.isd_lbl7.configure(text="Βιομηχ. Συμβόλαια: ")
    gui.isd_lbl7.place(x=640, y=340)
    gui.isd_input7.place(x=750, y=340)

    gui.isd_lbl8.configure(text="Αγροτ. Συμβόλαια: ")
    gui.isd_lbl8.place(x=940, y=340)
    gui.isd_input8.place(x=1050, y=340)

    gui.isd_lbl9.configure(text="ID Υποσταθμού: ")
    gui.isd_lbl9.place(x=640, y=400)
    gui.dropmn8.place(x=750, y=400)
    #gui.isd_input9.place(x=740, y=400)

    gui.exe_btn.place(x=640, y=460)
    gui.exe_btn.configure(command=lambda: ExeInsertArea(gui))

    return


def InsertCompany(gui):
    ClearRightGui(gui)

    gui.results_title.configure(text="Δεδομένα εισαγωγής:")

    gui.isd_lbl1.configure(text="ID: ")
    gui.isd_lbl1.place(x=640, y=160)
    gui.isd_input1.place(x=680, y=160)

    gui.isd_lbl2.configure(text="Όνομα: ")
    gui.isd_lbl2.place(x=940, y=160)
    gui.isd_input2.place(x=980, y=160)

    gui.isd_lbl3.configure(text="Έδρα: ")
    gui.isd_lbl3.place(x=640, y=220)
    gui.isd_input3.place(x=710, y=220)

    gui.isd_lbl4.configure(text="ID Σταθμού: ")
    gui.isd_lbl4.place(x=940, y=220)
    # gui.isd_input4.place(x=1020, y=220)
    gui.dropmn2.place(x=1020, y=220)


    gui.exe_btn.place(x=640, y=280)
    gui.exe_btn.configure(command=lambda: ExeInsertCompany(gui))

    return


def ExeInsertDiesp(gui):
    query = """ INSERT INTO `Διεσπαρμένη Παραγωγή` 
           (`ID Μονάδας Παραγωγής`, `Όνομα Σταθμού`, `Εγκατεστημένη Ισχύς (MW)`,
            `Μορφή Ενέργειας`, `Ενέργεια`, `Τεχνολογία`, `Γεωγρ. Μήκος`,
            `Γεωγρ. Πλάτος`, `Διαμέρισμα`, `Νομός`, `Ενεργός Από:`, 
            `Επίπεδο Τάσης Σύνδεσης (kV)`) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """

    values = (gui.isd_input1.get(), gui.isd_input2.get(), gui.isd_input3.get(),
              gui.isd_input4.get(), gui.isd_input5.get(), gui.isd_input6.get(),
              gui.isd_input7.get(), gui.isd_input8.get(), gui.isd_input9.get(),
              gui.isd_input10.get(), gui.isd_input11.get(), gui.isd_input12.get())

    try:
        cursor.execute(query, values)

    except (sql.Error, sql.Warning) as e:
        error = str(e)
        gui.isd_status.configure(text="Σφάλμα: " + error[error.find('"') + 1:error.rfind('"')])
        gui.isd_status.place(x=640, y=600)
        return

    gui.isd_status.configure(text="Η προσθήκη έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=600)

    return


def ExeInsertSubstation(gui):
    query = """INSERT INTO `Τοπικός Υποσταθμός`
            (`ID Υποσταθμού`, `Όνομα Σταθμού`, `Γεωγρ. Μήκος`, `Γεωγρ. Πλάτος`,
             `Διαμέρισμα`, `Νομός`, `Μετασχηματισμός Τάσης`, `Ενεργός Από`,
             `Συχνότητα (Hz)`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """

    values = (gui.isd_input1.get(), gui.isd_input2.get(), gui.isd_input3.get(),
              gui.isd_input4.get(), gui.isd_input5.get(), gui.isd_input6.get(),
              gui.isd_input7.get(), gui.isd_input8.get(), gui.isd_input9.get())

    try:
        cursor.execute(query, values)

    except (sql.Error, sql.Warning) as e:
        error = str(e)
        gui.isd_status.configure(text="Σφάλμα: " + error[error.find('"') + 1:error.rfind('"')])
        gui.isd_status.place(x=640, y=500)
        return

    gui.isd_status.configure(text="Η προσθήκη έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)

    return


def ExeInsertArea(gui):
    query = """INSERT INTO `Κατανάλωση Περιοχής`
            (`Περιοχή`, `Τ.Κ.`, `Νομός`, `Διαμέρισμα`,
             `Οικιακά Συμβόλαια`, `Εταιρικά Συμβόλαια`, `Βιομηχανικά Συμβόλαια`,
             `Αγροτικά Συμβόλαια`, `ID Βασικού Υποσταθμού`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """

    values = (gui.isd_input1.get(), gui.isd_input2.get(), gui.isd_input3.get(),
              gui.isd_input4.get(), gui.isd_input5.get(), gui.isd_input6.get(),
              gui.isd_input7.get(), gui.isd_input8.get(), gui.clicked8.get())

    try:
        cursor.execute(query, values)

    except (sql.Error, sql.Warning) as e:
        error = str(e)
        gui.isd_status.configure(text="Σφάλμα: " + error[error.find('"') + 1:error.rfind('"')])
        gui.isd_status.place(x=640, y=500)
        return

    gui.isd_status.configure(text="Η προσθήκη έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=500)

    return


def ExeInsertCompany(gui):
    query = """INSERT INTO `Εταιρεία`
            (`ID Εταιρείας`, `Όνομα Εταιρείας`, `Έδρα Εταιρείας`,
             `ID Διεσπαρμένης παραγωγής`)
            VALUES(%s, %s, %s, %s);"""

    values = (gui.isd_input1.get(), gui.isd_input2.get(), gui.isd_input3.get(),
              gui.clicked2.get())

    try:
        cursor.execute(query, values)

    except (sql.Error, sql.Warning) as e:
        error = str(e)
        gui.isd_status.configure(text="Σφάλμα: " + error[error.find('"') + 1:error.rfind('"')])
        gui.isd_status.place(x=640, y=300)
        return

    gui.isd_status.configure(text="Η προσθήκη έγινε επιτυχώς!")
    gui.isd_status.place(x=640, y=300)

    return


def get_companies_names():
    query = "SELECT DISTINCT `Όνομα Εταιρείας` " \
            "FROM `Εταιρεία`" \
            "ORDER BY `Όνομα Εταιρείας` ASC "
    opt = cursor.execute(query)
    opt = cursor.fetchall()
    dataframe = pd.DataFrame(opt)
    opt = dataframe['Όνομα Εταιρείας'].values.tolist()
    return opt


def get_station_names():
    query = "SELECT DISTINCT `Όνομα Σταθμού` " \
            "FROM `Διεσπαρμένη Παραγωγή`" \
            "ORDER BY `Όνομα Σταθμού` ASC "
    opt1 = cursor.execute(query)
    opt1 = cursor.fetchall()
    dataframe = pd.DataFrame(opt1)
    opt1 = dataframe['Όνομα Σταθμού'].values.tolist()
    return opt1


def getsubstation_name():
    query = "SELECT DISTINCT `Όνομα Σταθμού` " \
            "FROM `Τοπικός Υποσταθμός`" \
            "ORDER BY `Όνομα Σταθμού` ASC "
    opt2 = cursor.execute(query)
    opt2 = cursor.fetchall()
    dataframe = pd.DataFrame(opt2)
    opt2 = dataframe['Όνομα Σταθμού'].values.tolist()
    return opt2


def getarea():
    query = "SELECT DISTINCT `Περιοχή` " \
            "FROM `Κατανάλωση Περιοχής`" \
            "ORDER BY `Περιοχή` ASC "
    opt3 = cursor.execute(query)
    opt3 = cursor.fetchall()
    dataframe = pd.DataFrame(opt3)
    opt3 = dataframe['Περιοχή'].values.tolist()
    return opt3


def nomoi():
    query = "SELECT DISTINCT `Νομός` " \
            "FROM `Διεσπαρμένη Παραγωγή`" \
            "ORDER BY `Νομός` ASC "
    opt4 = cursor.execute(query)
    opt4 = cursor.fetchall()
    dataframe = pd.DataFrame(opt4)
    opt4 = dataframe['Νομός'].values.tolist()
    return opt4

def id():
    query = "SELECT `ID Υποσταθμού` " \
            "FROM `Τοπικός Υποσταθμός`" \
            "ORDER BY `ID Υποσταθμού`"

    opt5 = cursor.execute(query)
    opt5 = cursor.fetchall()
    dataframe = pd.DataFrame(opt5)
    opt5 = dataframe['ID Υποσταθμού'].values.tolist()
    return opt5


if __name__ == '__main__':
    cursor = ConnectDatabase()
    options2 = get_station_names()
    options4 = get_companies_names()
    options5 = getsubstation_name()
    options6 = getarea()
    options7 = nomoi()
    options8 = id()
    StartMenu(cursor)
