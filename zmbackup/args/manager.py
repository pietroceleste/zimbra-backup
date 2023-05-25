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
    
    def addLong(self, label, action = None, requireParameter=True): 
        postfix = '=' if requireParameter else ''        
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
        if (helpShortOption):
            self.addShort(helpShortOption, self.printHelp)
        if (helpLongOption):
            self.addLong(helpLongOption, self.printHelp, False)
        
    def printHelp(self):        
        print(self.helpMessage)
        sys.exit(2)
    
    def execute(self):
        cmdExec = False
        longOptions = self.longOptions.keys()
        for rawOption, arg in self.getOptions():
            curOption = rawOption.replace('--','') + '='            
            if (curOption in longOptions):
                self.longOptions[curOption](arg)
                cmdExec = True
            if (curOption.replace('=','') in longOptions):
                self.longOptions[curOption.replace('=','')]()
                cmdExec = True
        return cmdExec