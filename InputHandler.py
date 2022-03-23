from KaffeDB import KaffeDB
import pandas as pd

class InputHandler :

    loggedInUser = None
    kaffeDB = None

    def __init__(self):
        self.kaffeDB = KaffeDB()
        self.kaffeDB.connect("KaffeDB.db")

    #inputString = ""
    inputRequestMessage = "Input a command (type 'help' for a list of commands): "
    outputMessage = ""
    exit = False



    def printTable(self, header, table):
        if (table != None):
            df = pd.DataFrame(table, None, header)
            print(df)
        else:
            print("\n------------ Tabbellen er tom ------------\n")

    def shouldExit(self):
        return self.exit

    #def _setInputString (self, str):
    #    self.inputString = str
    
    def getInputRequestMessage (self) :
        return self.inputRequestMessage

    def clearOutputMessage (self) :
        self.outputMessage = None

    def registerReview(self):
        print("Registrert kaffe: ")
        self.printTable(self.kaffeDB.getCoffeeNames())
        coffeeName = input("Navn på kaffe: ")
        print("Registrerte kaffebrennerier: ")
        self.printTable(self.kaffeDB.getBreweies())
        breweryName = input("Navn på kaffebrenneri: ")
        breweryLocation = input ("Lokasjon på kaffebrenneri: ") 
        # TODO: Validate all feilds against database
        rating = input ("Antall poeng (1-10): ") # TODO: Add type checking + validation
        review = input ("Smaksnotat (beskrivelse på kaffeopplevelsen): ")
        # TODO : Insert a new review into the database

    def register (self):
        email = input("Brukernavn: ")
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
        #self._setInputString(str)
        if (str.lower() == "help"):
            self.outputMessage = "Liste av kommandoer: \n - anmeldelser \n - login \n - registrer \n - anmeld \n - toppliste \n - søk \n - beste-verdi\n"
        elif (str.lower() == "exit"):
            self.exit = True
        elif (str.lower() == "login"):
            email = input("E-post: ")
            password = input("Passord: ")
            self.login(email, password)
        elif (str.lower() == "registrer"):
            self.register()
        elif (str.lower() == "anmeldelser"):
            self.printTable(self.kaffeDB.getReviews())
        elif (str.lower() == "anmeld"):
            if (self.loggedInUser):
                self.registerReview()
            else:
                self.outputMessage = "Du må logge inn med en registrert bruker for å kunne legge inn kaffesmaking!"
        elif (str.lower() == "toppliste"):
            print ("toplist: ")
            self.printTable(self.kaffeDB.topList())
        elif (str.lower() == "søk"):
            keyword = input("Søkeord: ")
            table = (self.kaffeDB.search(keyword))
            self.printTable(table[0],table[1])
            
        elif (str.lower() == "beste-verdi"):
            # TODO: Execute best-value command
            self.outputMessage = "Best value: "
            

            
    