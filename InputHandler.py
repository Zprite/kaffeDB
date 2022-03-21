class InputHandler :
    
    inputString = ""
    inputRequestMessage = "Input a command (type 'help' for a list of commands): "
    outputMessage = ""

    def _setInputString (self, str):
        self.inputString = str
    
    def getInputRequestMessage (self) :
        return self.inputRequestMessage

    def handleInput(self, str):
        self._setInputString(str)

        if (str.lower() == "help"):
            self.outputMessage = "List of commands: \n - login \n - register \n - review \n - toplist \n - search \n - best-value"

    