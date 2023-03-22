import getopt, sys

class manager:
    
    helpMessage = "Help message is not defined"
    shortOptions = {}
    longOptions = {}
    reqOptions = None      

    def init(self, rawArgv):        
        self.reqOptions, self.args = getopt.getopt(rawArgv, self.shortOptions, self.longOptions.keys())        

    def addShort(self, label, action = None):        
            self.shortOptions[label] = action
    
    def addLong(self, label, action = None, postfix = "="):        
            self.longOptions[label.replace('--','') + postfix] = action

    def validateRequiredParameters(self, requiredOptions):
        for requiredOption in requiredOptions:
            if (not self.optionExists(requiredOption)):
                raise ValueError("Parameter %s is required" % requiredOption)
    
    def optionExists(self, requestOption):
        for currentOption, arg in self.reqOptions:
            if (currentOption == requestOption):
                return True
        return False
            
    def getOption(self, requestOption, defaultValue = None): 
        for currentOption, arg in self.reqOptions:
            if (currentOption == requestOption):
                return arg
        if (defaultValue != None):
            return defaultValue
        else :
            raise ValueError("Parameter %s is required" % requestOption)
    
    def getOptions(self):
        return self.reqOptions
    
    def setHelpMessage(self, helpMessage, helpShortOption = "h", helpLongOption = "--help"):
        self.helpMessage = helpMessage
        
    def printHelp(self):        
        print(self.helpMessage)
        sys.exit(2)
    
    def execute(self):
        cmdExec = False        
        for rawOption, arg in self.getOptions():
            option = rawOption.replace('--','') + '='
            if option in self.longOptions.keys():
                self.longOptions[option](arg)
                cmdExec= True
        return cmdExec