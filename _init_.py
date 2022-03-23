from UserController import UserController
from Utils import Utils

#Utils.deleteDB()
#Utils.runSqlScript()

UC = UserController()

while (UC.shouldExit() != True):
    UC.handleInput(input(UC.getInputRequestMessage()))
