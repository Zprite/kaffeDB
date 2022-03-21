import KaffeDB

class InputHandler :

    def __init__(self):
        self.kaffeDB = KaffeDB()
        self.kaffeDB.connect("KaffeDB.db")

    #inputString = ""
    inputRequestMessage = "Input a command (type 'help' for a list of commands): "
    outputMessage = ""
    exit = False

    def shouldExit(self):
        return self.exit

    #def _setInputString (self, str):
    #    self.inputString = str
    
    def getInputRequestMessage (self) :
        return self.inputRequestMessage

    def clearOutputMessage (self) :
        self.outputMessage = None

    def handleInput(self, str):
        #self._setInputString(str)
        if (str.lower() == "help"):
            self.outputMessage = "Liste av kommandoer: \n - login \n - registrer \n - kaffesmaking \n - toppliste \n - søk \n - beste-verdi\n"
        elif (str.lower() == "exit"):
            self.exit = True
        elif (str.lower() == "login"):
            email = input("E-post: ")
            password = input("Passord: ")
        elif (str.lower() == "registrer"):
            email = input("Brukernavn: ")
            password = input("Passord: ")
            firstName = input ("Fornavn: ")
            lastName = input("Etternavn: ")
        elif (str.lower() == "kaffesmaking"):
            # TODO: print table with all UNIQUE coffee-names
            coffeeName = input("Navn på kaffe: ")
            # TODO: print table with all breweries (NAME + LOCATION) associated with said cofee-name
            breweryName = input("Navn på kaffebrenneri: ")
            breweryLocation = input ("Lokasjon på kaffebrenneri: ") 
            # TODO: Validate all feilds against database
            rating = input ("Antall poeng (1-10): ") # TODO: Add type checking + validation
            review = input ("Smaksnotat (beskrivelse på kaffeopplevelsen): ")
            # TODO : Insert a new review into the database
        elif (str.lower() == "toppliste"):
            self.outputMessage = "toplist: "
            self.kaffeDB.toplist()
        elif (str.lower() == "søk"):
            # TODO: vanskelig metode :(
            self.outputMessage = ""
        elif (str.lower() == "beste-verdi"):
            # TODO: Execute best-value command
            self.outputMessage = "Best value: "
            

            
    