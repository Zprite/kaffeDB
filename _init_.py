from InputHandler import InputHandler
from KaffeDB import KaffeDB
from Utils import Utils
from InputHandler import InputHandler

Utils.deleteDB()
Utils.runSqlScript()

IH = InputHandler()

while (IH.shouldExit() != True):
    IH.handleInput(input(IH.getInputRequestMessage()))

#kaffeDB.showAllItems("Ferdigbrentkaffe")
#kaffeDB.getParameter("FerdigbrentKaffe", "ID", "1", "Navn")
#kaffeDB.getItem("FerdigbrentKaffe", "ID", "2")
#kaffeDB.registerUser("testbruker@kaffeDB.no", "test123", "test", "bruker")
#kaffeDB.review("testbruker@kaffeDB.no", 1, "Dette er en fortreffelig kaffe. 10/10!", 10, "2022-03-18") #vil feile når sjekken for registrert bruker er implementert
#kaffeDB.showAllItems("Kaffesmaking")