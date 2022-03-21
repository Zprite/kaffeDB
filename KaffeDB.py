import sqlite3


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
        print(self.cursor.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]) #Kan fjernes når appen er komplett
        return self.cursor.execute(f'SELECT {parameterName} FROM {table} WHERE {pkName}={pkValue}').fetchone()[0]

    #Henter alle brukere i kaffesmaking tabellen, sortert etter hvor mange kaffer som brukeren har smakt på
    def topList(self):
        request = 'SELECT Fornavn, Etternavn, COUNT(BrukerEpost) FROM Kaffesmaking LEFT JOIN Bruker ON Kaffesmaking.BrukerEpost = Bruker.Epost GROUP BY BrukerEpost ORDER BY COUNT(BrukerEpost) DESC'
        for row in self.connection.execute(request).fetchall():
            print(row)

    #Legger til en bruker i Bruker tabellen dersom eposten ikke eksisterer i tabellen fra før
    def registerUser(self, userMail, password, firstName, lastName):
        #TODO sjekk om eposten faktisk er en epost (hvis nødvendig)
        if self.cursor.execute('SELECT * FROM Bruker WHERE Epost=?', (userMail,)).fetchone() == None:
            self.cursor.execute('INSERT INTO Bruker VALUES (?, ?, ?, ?)', (userMail, password, firstName, lastName))
            self.connection.commit()
        else:
            print('Brukeren eksisterer allerede i databasen')

    #Legger til et element i Kaffesmaking tabellen
    def review(self, userMail, coffeeID, note, score, date):
        #TODO Sjekk at mailen ligger i databasen fra før
        if self.cursor.execute('SELECT * FROM Kaffesmaking WHERE BrukerEpost=? AND FerdigbrentKaffeID=?', (userMail, coffeeID,)).fetchone() == None:
            self.cursor.execute('INSERT INTO Kaffesmaking VALUES (?, ?, ?, ?, ?)', (userMail, coffeeID, note, score, date))
            self.connection.commit()
        else:
            print('Denne brukeren har allerede smakt på denne kaffen')
