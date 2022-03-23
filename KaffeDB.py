import re
import sqlite3
from typing import Tuple
from xmlrpc.client import DateTime
#import pandas as pd

class KaffeDB:
    connection = None
    cursor = None

    def connect(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
    
    #For testingen sin del, denne viser alle tuplene i en tabell
    def showAllItems(self, table):
        try:
            for row in self.cursor.execute(f'SELECT * FROM {table};'):
                print(row)
        except sqlite3.OperationalError:
            print(f'Tabellen {table} finnes ikke i databasen')
    
    #Henter ut en tuppel fra en tabell basert på tabellnavn, navn på primary key og verdien på primary key
    def getItem(self, table, pkName, pkValue):
        print(self.cursor.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}').fetchone()) #Kan fjernes når appen er komplett
        return self.cursor.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}').fetchone()
    
    #Henter ut et parameter fra et element i en tabell (kanskje ikke nødvendig)
    def getParameter(self, table, pkName, pkValue, parameterName):
        print(self.cursor.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]) #Kan fjernes når appen er komplet
        return self.cursor.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]

    def getTable(self, table):
        return self.cursor.execute(f'SELECT * FROM {table}').fetchall()
    def getCoffeeNames(self):
        return self.cursor.execute('SELECT Navn FROM FerdigbrentKaffe').fetchall()
    def getBreweies(self):
        return self.cursor.execute('SELECT Navn, Lokasjon FROM Kaffebrenneri').fetchall()

    #Henter alle brukere i kaffesmaking tabellen, sortert etter hvor mange kaffer som brukeren har smakt på
    def topList(self):
        request = 'SELECT Fornavn, Etternavn, COUNT(BrukerEpost) FROM Kaffesmaking LEFT JOIN Bruker ON Kaffesmaking.BrukerEpost = Bruker.Epost GROUP BY BrukerEpost ORDER BY COUNT(BrukerEpost) DESC'
        return self.cursor.execute(request).fetchall()

    #Legger til en bruker i Bruker tabellen dersom eposten ikke eksisterer i tabellen fra før
    def registerUser(self, email, password, firstName, lastName):
        #TODO sjekk om eposten faktisk er en epost (hvis nødvendig)
        if self.cursor.execute('SELECT * FROM Bruker WHERE Epost=?', (email,)).fetchone() == None:
            self.cursor.execute('INSERT INTO Bruker VALUES (?, ?, ?, ?)', (email, password, firstName, lastName))
            self.connection.commit()
        else:
            print('Brukeren eksisterer allerede i databasen')

    # Sjekker om bruker med passord finnes i systemet
    # NB: Applikasjonen bruker ikke sikker passordlagring for enkelhets skyld. Aldri lagre passord som plaintext i ekte applikasjoner.
    def authenticateUser(self, email, password):
        return not (self.cursor.execute('SELECT * FROM Bruker WHERE Epost=? AND Passord=?', (email,password)).fetchone() == None)
    #Legger til et element i Kaffesmaking tabellen
    def review(self, email, score, note, coffeeName, breweryName, breweryLocation):
        if not (self.cursor.execute('SELECT * FROM Bruker WHERE Epost=?', (email,)).fetchone() == None):
            breweryID = self.cursor.execute('SELECT ID FROM Kaffebrenneri WHERE Navn=? AND Location=?', (breweryName, breweryLocation)).fetchone()
            # Hent den siste kaffen, ettersom kaffenavn + kaffebrenneriID ikke er en komplett nøkkel for tabellen.
            coffeeID = self.cursor.execute('SELECT ID FROM FerdigbrentKaffe WHERE Navn=? AND KaffebrenneriID=?', (coffeeName, breweryID)).fetchone()
            if self.cursor.execute('SELECT * FROM Kaffesmaking WHERE BrukerEpost=? AND FerdigbrentKaffeID=?', (email, coffeeID,)).fetchone() == None:
                print(coffeeID + email + note + score)
                self.cursor.execute('INSERT INTO Kaffesmaking VALUES (?, ?, ?, ?, CURRENT_DATE)', (email, coffeeID, note, score))
                self.connection.commit()
            else:
                print('Denne brukeren har allerede smakt på denne kaffen')
    def getReviews(self):
        request = """SELECT Smaksnotat, AntallPoeng, FerdigbrentKaffe.Navn 
        FROM Kaffesmaking INNER JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe.ID 
        INNER JOIN Bruker ON BrukerEpost = Bruker.Epost """
        self.cursor.execute(request).fetchone()

    #Skriver ut navnet på kaffen og brenneriet hvor enten en bruker eller et brenneri har beskrevet kaffen med et nøkkelord
    def search (self, keyword):
        request = '''SELECT FerdigbrentKaffe.Navn, Kaffebrenneri.Navn FROM FerdigbrentKaffe 
        LEFT JOIN Kaffesmaking ON FerdigbrentKaffe.ID = Kaffesmaking.FerdigbrentKaffeID INNER JOIN Kaffebrenneri ON FerdigbrentKaffe.KaffebrenneriID = Kaffebrenneri.ID 
        WHERE FerdigbrentKaffe.Beskrivelse LIKE ? OR Kaffesmaking.Smaksnotat LIKE ? GROUP BY FerdigbrentKaffe.ID'''
        return(("Navn på Kaffe", "Kaffebrenneri"), (self.cursor.execute(request, ('%'+keyword+'%', '%'+keyword+'%')).fetchall()))