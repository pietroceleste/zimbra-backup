import os
import json

class filesystem:
    
    def scanBackupDirectory(self, rootDir):
        result = {}
        for root, dirs, files in os.walk(rootDir):            
            for currentDirectory in dirs:
                size = self._calculateDirSize(rootDir + '\\' + currentDirectory)
                result[currentDirectory] = size
        return result

    def _calculateDirSize(self, path):        
        result = 0        
        for root, dirs, files in os.walk(path):            
            total_size = sum(os.path.getsize(os.path.join(root, name)) for name in files)            
            result += total_size        
        return result

    def getJsonFile(self, filePath):
        if (not os.path.exists(filePath)):
            raise Exception("Il file %s non esiste" % filePath)
        with open(filePath, "r") as json_file:            
            return json.load(json_file)

    def getZeroSizeSubDirectory(self, rootDir):
        result = []        
        backupSubDirs = self.scanBackupDirectory(rootDir)
        for subDir in backupSubDirs:
            size = backupSubDirs[subDir]
            if (size > 0):
                continue
            result.append(subDir)
        return result

    def getSubDirectory(self, rootDir):
        result = []
        for root, dirs, files in os.walk(rootDir):            
            for currentDirectory in dirs:                
                result.append(currentDirectory)
        return result
    
    def saveFile(self, fileName, fileContent, method = "wb"):        
        self.createPathIfNotExixts(fileName)
        fileHandle = open(fileName, method)
        fileHandle.write(fileContent)
        fileHandle.close()

    def createPathIfNotExixts(self, rawPath):
        path = os.path.dirname(rawPath.replace("\\","/"))        
        if (path and not os.path.exists(path)):
            print('Creo la directory %s.' , (path))
            os.makedirs(path)