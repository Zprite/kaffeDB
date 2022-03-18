import sqlite3

class KaffeDB:
    connection = None
    def connect(self, path):
        self.connection = sqlite3.connect(path)
    
    def showAllItems(self, table):
        try:
            for row in self.connection.execute(f'SELECT * FROM {table};'):
                print(row)
        except sqlite3.OperationalError:
            print(f'Tabellen {table} finnes ikke i databasen')
    
    def getItem(self, table, pkName, pkValue):
        print(self.connection.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}').fetchone())
    
    def getParameter(self, table, pkName, pkValue, parameterName):
        print(self.connection.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0])

    def review(self, userMail, coffeeID, note, score, date):
        #TODO Sjekk at mailen ligger i databasen fra før
        if self.connection.execute('SELECT * FROM Kaffesmaking WHERE BrukerEpost=? AND FerdigbrentKaffeID=?', (userMail, coffeeID,)).fetchone() == None:
            self.connection.execute('INSERT INTO Kaffesmaking VALUES (?, ?, ?, ?, ?)', (userMail, coffeeID, note, score, date))
            self.connection.commit()
        else:
            print('Denne brukeren har allerede smakt på denne kaffen')

kaffeDB = KaffeDB() #Det må være en instans av klassen for at metodene skal fungere
kaffeDB.connect("KaffeDB.db") #Denne må kjøres før andre klassemetoder
kaffeDB.showAllItems("Ferdigbrentkaffe")
kaffeDB.getParameter("FerdigbrentKaffe", "ID", "1", "Navn")
kaffeDB.getItem("FerdigbrentKaffe", "ID", "2")
kaffeDB.review("testbruker@kaffeDB.no", 1, "Dette er en fortreffende kaffe. 10/10!", 10, "2022-03-18") #vil feile når sjekken for registrert bruker er implementert
kaffeDB.showAllItems("Kaffesmaking")