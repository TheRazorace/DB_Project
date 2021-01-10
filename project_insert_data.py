# -*- coding: utf-8 -*-

#Απαραίτητες βιβλιοθήκες
import pymysql as sql
import pymysql.cursors as cur
import pandas as pd
import random 

#Σύνδεση με τη βάση δεδομένων
def ConnectDatabase():
    
    connection = sql.connect (host = "150.140.186.221",
                  port = 3306,
                  user = "db20_up1047398",
                  password = "up1047398",
                  db = "project_db20_up1047398",
                  charset = "utf8mb4",
                  cursorclass=cur.DictCursor)
    
    connection.autocommit(True)
    
    cursor = connection.cursor()  
    
    return cursor

#Συνάρτηση εισαγωγής μετρήσεων κατανάλωσης
def InsertConsumed(cursor):
    
    # Αποθήκευση περιοχών
    query = "SELECT * FROM `Κατανάλωση Περιοχής`"
    cursor.execute(query)
    data=cursor.fetchall()
    df = pd.DataFrame(data)
    size = len(df)
    
    # Λεπτά για μία ώρα ανά τέταρτο
    minutes = [0]*4
    minutes[0] = "00"
    minutes[1] = "15"
    minutes[2] = "30"
    minutes[3] = "45"
    
    # Ημερομηνία μέτρησης
    date = "2021-01-15 "
    
    # Αρχικοποίηση πινάκων
    areas = [0]*size
    tk = [0]*size
    county = [0]*size
    consumption = [0]*size
    
    # Δημιουργία μιας κατανάλωσης βάσει των συμβολαίων κάθε περιοχής
    for index, row in df.iterrows():
        areas[index] = row['Περιοχή'] 
        tk[index] = row['Τ.Κ.']
        county[index] = row['Νομός']
        consumption[index] = float(row['Οικιακά Συμβόλαια'] +
                                   row['Εταιρικά Συμβόλαια']*5 +
                                   row['Βιομηχανικά Συμβόλαια']*20 +
                                   row['Αγροτικά Συμβόλαια']*7)/15
      
    # Εισαγωγή στην βάση
    for i in range (0, len(areas)):
        for k in range (0, len(minutes)):
                
            query = """ INSERT INTO `Μέτρηση Κατανάλωσης` 
            (`Ώρα`, `Περιοχή`, `Τ.Κ.`, `Νομός`, `Συνολική Κατανάλωση (KWh)`) 
            VALUES (%s, %s, %s, %s, %s); """
    
            datetime = date + "12:" + minutes[k] + ":00"
            
            # Προσθήκη μικρής τυχαιότητας στις μετρήσεις
            cur_cons = consumption[i] + round(random.uniform(0,consumption[i]/4), 2)
            
            #Εκτέλεση query
            insert_data = (datetime, areas[i], tk[i], county[i], cur_cons)
            cursor.execute(query, insert_data)
    
    return

# Συνάρτησης εισαγωγής μετρήσεων παραγωγής
def InsertProduced(cursor):
    
    #Αποθήκευση σταθμών παραγωγής
    query = "SELECT * FROM `Διεσπαρμένη Παραγωγή`"
    cursor.execute(query)
    data=cursor.fetchall()
    df = pd.DataFrame(data)
    size = len(df)
    
    # Λεπτά για μία ώρα ανά τέταρτο
    minutes = [0]*4
    minutes[0] = "00"
    minutes[1] = "15"
    minutes[2] = "30"
    minutes[3] = "45"
        
    # Ημερομηνία μέτρησης    
    date = "2021-01-15 "
    
    # Αρχικοποίηση πινάκων
    ids = [0]*size
    production = [0]*size
    
    #Δημιουργία μιας μέτρησης ανάλογα της εγκατεστημένης ισχύος των σταθμών
    for index, row in df.iterrows():
        ids[index] = row['ID Μονάδας Παραγωγής']
        production[index] = float(row['Εγκατεστημένη Ισχύς (MW)'] * 1000 * 0.25 * 0.25 * 0.6)
        #Απόδοση 0.25
        #Ανά τέταρτο (0.25)
        #Σε λειτουργεία 60% της ονομαστικής τάσης (0.6)
        
    
    #Εισαγωγή στην βάση
    for i in range (0, len(ids)):
       for k in range (0, len(minutes)):
                
           query = """ INSERT INTO `Μέτρηση Παραγωγής` 
           (`Ώρα`, `Συνολική Μέτρηση (KWh)`, `ID Μονάδας Παραγωγής`) 
           VALUES (%s, %s, %s); """   
           
           datetime = date + "12:" + minutes[k] + ":00"
           
           #Προσθήκη μικρής τυχαιότητας 
           cur_prod = production[i] + round(random.uniform(-production[i]/5,production[i]/5), 2)
           
           #Εκτέλεση query
           insert_data = (datetime, cur_prod, ids[i])
           cursor.execute(query, insert_data)
    
    return

if __name__ == '__main__':  

    cursor = ConnectDatabase()
    #InsertConsumed(cursor)
    #InsertProduced(cursor)
