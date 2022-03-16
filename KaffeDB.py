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
            print(f"Tabellen {table} finnes ikke i databasen")
    
    def getItem(self, table, pkName, pkValue):
        for row in self.connection.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}'):
            print(row)
    
    def getParameter(self, table, pkName, pkValue, parameterName):
        for row in self.connection.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}'):
            print(row)

kaffeDB = KaffeDB() #Det må være en instans av klassen for at metodene skal fungere
kaffeDB.connect("KaffeDB.db") #Denne må kjøres før andre klassemetoder
kaffeDB.showAllItems("Ferdigbrentkaffe")
kaffeDB.getParameter("FerdigbrentKaffe", "ID", "1", "Navn")
kaffeDB.getItem("FerdigbrentKaffe", "ID", "2")