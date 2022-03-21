from InputHandler import InputHandler
from KaffeDB import KaffeDB
from Utils import Utils
from InputHandler import InputHandler

Utils.deleteDB()
Utils.runSqlScript()
kaffeDB = KaffeDB() #Det må være en instans av klassen for at metodene skal fungere
kaffeDB.connect("KaffeDB.db") #Denne må kjøres før andre klassemetoder (Den laster inn databasen)

exit = False
IH = InputHandler()

while (IH.shouldExit() != True):
    IH.handleInput(input(IH.getInputRequestMessage()))
    if (IH.outputMessage):
        print(IH.outputMessage)
        IH.clearOutputMessage()

#kaffeDB.showAllItems("Ferdigbrentkaffe")
#kaffeDB.getParameter("FerdigbrentKaffe", "ID", "1", "Navn")
#kaffeDB.getItem("FerdigbrentKaffe", "ID", "2")
#kaffeDB.registerUser("testbruker@kaffeDB.no", "test123", "test", "bruker")
#kaffeDB.review("testbruker@kaffeDB.no", 1, "Dette er en fortreffelig kaffe. 10/10!", 10, "2022-03-18") #vil feile når sjekken for registrert bruker er implementert
#kaffeDB.showAllItems("Kaffesmaking")