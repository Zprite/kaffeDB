from UserController import UserController
from Utils import Utils

#Utils.deleteDB()
#Utils.runSqlScript()

UC = UserController()
print("---- Velkommen til kaffedb! ----")
while (UC.shouldExit() != True):
    UC.handleInput(input(UC.getInputRequestMessage()))
