from KaffeDB import KaffeDB
import pandas as pd

class UserController :
    loggedInUser = None
    kaffeDB = None
    inputRequestMessage = "Skriv inn kommando ('hjelp' for en liste med kommandoer): "
    
    # Set to true to exit the program
    exit = False

    def __init__(self):
        self.kaffeDB = KaffeDB()
        self.kaffeDB.connect("KaffeDB.db")

    def printTable(self, tableName, table,):
        if (table != None and len(table[1]) > 0):
            header = table[0]
            data = table[1]
            print(f"\n------------ {tableName} ------------\n")
            df = pd.DataFrame(data, None, header)
            print(df , "\n")
        else:
            print("\n------------ Tabbellen er tom ------------\n")

    def shouldExit(self):
        return self.exit
    
    def getInputRequestMessage (self) :
        return self.inputRequestMessage

    def registerReview(self):
        print("\nVenligst oppgi opplysninger om kaffen du har smakt: \n Registrert kaffe: ")
        self.printTable("Kaffe på brennerier", self.kaffeDB.getCoffeAndBrewery())
        coffeeName = input("Skriv inn navn på kaffe: ")
        breweryName = input("Skriv inn navn på kaffebrenneri: ")
        breweryLocation = input ("Skriv inn lokasjon på kaffebrenneri: ") 
        rating = None
        exit= False
        while (not exit):
            try:
                rating = int(input ("Antall poeng (1-10): "))
            except ValueError:
                print("Venligst skriv inn et tall fra 1-10")
            finally:
                if (rating not in range(1,11)):
                    print("Venligst skriv inn et tall fra 1-10")
                else:
                    exit = True
        note = input ("Smaksnotat (beskrivelse på kaffeopplevelsen): ")
        try:
            # Insert a new review into the database
            self.kaffeDB.postreview(self.loggedInUser, rating, note, coffeeName, breweryName, breweryLocation)
        except Exception as e:
            print("Klarte ikke å oprette kaffesmaking: ", e)

    def register (self):
        email = input("E-post: ")
        password = input("Passord: ")
        firstName = input ("Fornavn: ")
        lastName = input("Etternavn: ")
        self.kaffeDB.registerUser(email, password, firstName, lastName)
        self.login(email, password)

    def login (self, email, password):
        if(self.kaffeDB.authenticateUser(email, password)):
            self.loggedInUser = email
            print("Du er nå logget in!")
        else:
            print("Feil ved innlogging! Sjekk at epost og passord er riktig inntastet.")

    def handleInput(self, str):
        if (str.lower() == "hjelp"):
            print("""Liste av kommandoer: \n 
            - anmeldelser 
            - anmeld
            - beste-verdi
            - kaffebrennerier
            - login
            - registrer
            - søk 
            - toppliste
        """)
        elif (str.lower() == "exit"):
            self.exit = True
        elif (str.lower() == "login"):
            email = input("E-post: ")
            password = input("Passord: ")
            self.login(email, password)
        elif (str.lower() == "registrer"):
            self.register()
        elif (str.lower() == "anmeldelser"):
            self.printTable("Brukeranmeldelser", self.kaffeDB.getReviews())
        elif (str.lower() == "anmeld"):
            if (self.loggedInUser):
                self.registerReview()
            else:
                print("Du må logge inn med en registrert bruker for å kunne legge inn kaffesmaking!")
        elif (str.lower() == "kaffebrennerier"):
            self.printTable("Kaffebrennerier",self.kaffeDB.getBreweies())
        elif (str.lower() == "toppliste"):
            print ("toplist: ")
            self.printTable("Bruker-Toppliste", self.kaffeDB.topList())
        elif (str.lower() == "søk"):
            keyword = input("Søkeord: ")
            self.printTable("Søkeresultater", (self.kaffeDB.search(keyword)))
        elif (str.lower() == "beste-verdi"):
            # TODO: Execute best-value command
            print("Best value: ")
        else:
            print("Ugyldig kommando! Bruk 'hjelp' for en liste med kommandoer")
            

            
    