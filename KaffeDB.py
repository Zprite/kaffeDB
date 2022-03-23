import sqlite3

class KaffeDB:
    connection = None
    cursor = None

    def connect(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

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

    def postreview(self, email, score, note, coffeeName, breweryName, breweryLocation):
        # Sjekker at bruker eksisterer
        if not (self.cursor.execute('SELECT * FROM Bruker WHERE Epost=?', (email,)).fetchone() == None):
            breweryID = self.cursor.execute('SELECT ID FROM Kaffebrenneri WHERE Navn=? AND Lokasjon=?', (str(breweryName), str(breweryLocation))).fetchone()
            ## Feilhåndtering ved ugyldig brukerinput
            if (breweryID == None):
                raise Exception(f"Finner ingen kaffebrennerier med navn: {breweryName} og lokasjon: {breweryLocation}")
            breweryID = breweryID[0]
            # Hent den siste kaffen, ettersom kaffenavn + kaffebrenneriID ikke er en komplett nøkkel for tabellen.
            coffeeID = self.cursor.execute('SELECT ID FROM FerdigbrentKaffe WHERE Navn=? AND KaffebrenneriID=?', (str(coffeeName), int(breweryID))).fetchone()
            ## Feilhåndtering ved ugyldig brukerinput
            if (coffeeID == None):
                raise Exception(f"Finner ingen Kaffe med navn: {coffeeName} på kaffebrenneri: {breweryName}, {breweryLocation}")
            coffeeID = coffeeID[0]
            # Sjekker at ikke det finnes en kaffesmaking med samme kaffeID hos brukeren
            if  self.cursor.execute('SELECT * FROM Kaffesmaking WHERE BrukerEpost=? AND FerdigbrentKaffeID=?', (str(email), int(coffeeID))).fetchone() == None:
                print("Opretter kaffesmaking....")
                self.cursor.execute('INSERT INTO Kaffesmaking VALUES (?, ?, ?, ?, CURRENT_DATE)', (str(email), int(coffeeID), str(note), int(score)))
                self.connection.commit()
                print("--- Opretting av kaffesmaking var vellykket! ---")
            else:
                raise Exception('Denne brukeren har allerede smakt på denne kaffen')
                
    def getTable(self, table):
        return (tuple("Tabell") , self.cursor.execute(f'SELECT * FROM {table}').fetchall())
    def getCoffeeNames(self):
        return (tuple("Navn på Kaffe") , self.cursor.execute('SELECT Navn FROM FerdigbrentKaffe').fetchall())
    def getBreweies(self):
        return (("Kaffebrenneri" , "Lokasjon"), self.cursor.execute('SELECT Navn, Lokasjon FROM Kaffebrenneri').fetchall())
    def getCoffeAndBrewery(self):
        request = """Select FerdigbrentKaffe.Navn, Kaffebrenneri.Navn, Kaffebrenneri.Lokasjon
                FROM FerdigbrentKaffe INNER JOIN Kaffebrenneri ON (KaffebrenneriID = Kaffebrenneri.ID)"""
        return(("Navn på Kaffe", "Kaffebrenneri" , "Lokasjon"), self.cursor.execute(request).fetchall())

    #Henter alle brukere i kaffesmaking tabellen, sortert etter hvor mange kaffer som brukeren har smakt på
    def topList(self):
        request = """SELECT Fornavn, Etternavn, COUNT(BrukerEpost) 
        FROM Kaffesmaking LEFT JOIN Bruker ON (Kaffesmaking.BrukerEpost = Bruker.Epost) 
        GROUP BY BrukerEpost ORDER BY COUNT(BrukerEpost) DESC"""
        return (("Fornavn", "Etternavn", "Antall Anmeldelser"),self.cursor.execute(request).fetchall())
    # Henter alle anmeldelser i databasen
    def getReviews(self):
        request = """SELECT Bruker.Fornavn, FerdigbrentKaffe.Navn, Kaffebrenneri.Navn, Kaffebrenneri.Lokasjon, AntallPoeng, Smaksnotat 
        FROM Kaffesmaking INNER JOIN FerdigbrentKaffe ON FerdigbrentKaffeID = FerdigbrentKaffe.ID 
        INNER JOIN Bruker ON BrukerEpost = Bruker.Epost 
        INNER JOIN Kaffebrenneri ON KaffebrenneriID = Kaffebrenneri.ID"""
        return (("Bruker", "Navn på Kaffe", "Kaffebrenneri", "Lokasjon", "Poeng(1-10)", "Notat" ), self.cursor.execute(request).fetchall())

    #Skriver ut navnet på kaffen og brenneriet hvor enten en bruker eller et brenneri har beskrevet kaffen med et nøkkelord
    def search (self, keyword):
        request = '''SELECT FerdigbrentKaffe.Navn, Kaffebrenneri.Navn FROM FerdigbrentKaffe 
        LEFT JOIN Kaffesmaking ON FerdigbrentKaffe.ID = Kaffesmaking.FerdigbrentKaffeID 
        INNER JOIN Kaffebrenneri ON FerdigbrentKaffe.KaffebrenneriID = Kaffebrenneri.ID 
        WHERE FerdigbrentKaffe.Beskrivelse LIKE ? OR Kaffesmaking.Smaksnotat LIKE ? 
        GROUP BY FerdigbrentKaffe.ID'''
        return(("Navn på Kaffe", "Kaffebrenneri"), (self.cursor.execute(request, ('%'+keyword+'%', '%'+keyword+'%')).fetchall()))