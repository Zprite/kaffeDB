class InputHandler :
    
    inputString = ""
    inputRequestMessage = "Input a command (type 'help' for a list of commands): "
    outputMessage = ""
    exit = False

    def shouldExit(self):
        return self.exit

    def _setInputString (self, str):
        self.inputString = str
    
    def getInputRequestMessage (self) :
        return self.inputRequestMessage

    def clearOutputMessage (self) :
        self.outputMessage = None

    def handleInput(self, str):
        self._setInputString(str)
        if (str.lower() == "help"):
            self.outputMessage = "List of commands: \n - login \n - register \n - review \n - toplist \n - search \n - best-value"
        elif (str.lower() == "exit"):
            self.exit = True
            
    