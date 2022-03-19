import sqlite3

class KaffeDB:
    connection = None
    def connect(self, path):
        self.connection = sqlite3.connect(path)
    
    #For testingen sin del, denne viser alle tuplene i en tabell
    def showAllItems(self, table):
        try:
            for row in self.connection.execute(f'SELECT * FROM {table};'):
                print(row)
        except sqlite3.OperationalError:
            print(f'Tabellen {table} finnes ikke i databasen')
    
    #Henter ut en tuppel fra en tabell basert på tabellnavn, navn på primary key og verdien på primary key
    def getItem(self, table, pkName, pkValue):
        print(self.connection.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}').fetchone()) #Kan fjernes når appen er komplett
        return self.connection.execute(f'SELECT * FROM {table} WHERE {pkName}={pkValue}').fetchone()
    
    #Henter ut et parameter fra et element i en tabell (kanskje ikke nødvendig)
    def getParameter(self, table, pkName, pkValue, parameterName):
        print(self.connection.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]) #Kan fjernes når appen er komplett
        return self.connection.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]

    #Legger til en bruker i Bruker tabellen dersom eposten ikke eksisterer i tabellen fra før
    def registerUser(self, userMail, password, firstName, lastName):
        #TODO sjekk om eposten faktisk er en epost (hvis nødvendig)
        if self.connection.execute('SELECT * FROM Bruker WHERE Epost=?', (userMail,)).fetchone() == None:
            self.connection.execute('INSERT INTO Bruker VALUES (?, ?, ?, ?)', (userMail, password, firstName, lastName))
            self.connection.commit()
        else:
            print('Brukeren eksisterer allerede i databasen')

    #Legger til et element i Kaffesmaking tabellen
    def review(self, userMail, coffeeID, note, score, date):
        #TODO Sjekk at mailen ligger i databasen fra før
        if self.connection.execute('SELECT * FROM Kaffesmaking WHERE BrukerEpost=? AND FerdigbrentKaffeID=?', (userMail, coffeeID,)).fetchone() == None:
            self.connection.execute('INSERT INTO Kaffesmaking VALUES (?, ?, ?, ?, ?)', (userMail, coffeeID, note, score, date))
            self.connection.commit()
        else:
            print('Denne brukeren har allerede smakt på denne kaffen')

kaffeDB = KaffeDB() #Det må være en instans av klassen for at metodene skal fungere
kaffeDB.connect("KaffeDB.db") #Denne må kjøres før andre klassemetoder (Den laster inn databasen)
kaffeDB.showAllItems("Ferdigbrentkaffe")
kaffeDB.getParameter("FerdigbrentKaffe", "ID", "1", "Navn")
kaffeDB.getItem("FerdigbrentKaffe", "ID", "2")
kaffeDB.registerUser("testbruker@kaffeDB.no", "test123", "test", "bruker")
kaffeDB.review("testbruker@kaffeDB.no", 1, "Dette er en fortreffende kaffe. 10/10!", 10, "2022-03-18") #vil feile når sjekken for registrert bruker er implementert
kaffeDB.showAllItems("Kaffesmaking")