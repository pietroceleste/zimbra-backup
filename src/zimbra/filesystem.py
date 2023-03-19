import os
import json
import requests

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

    def downloadAndSaveBackupFile(self, url, localFilename, adminAccount):
        self.createPathIfNotExixts(localFilename)
        requests.packages.urllib3.disable_warnings()
        with requests.get(url, stream=True, verify=False, auth=tuple(adminAccount)) as r:
            r.raise_for_status()
            with open(localFilename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    f.write(chunk)

    def createPathIfNotExixts(self, rawPath):
        path = os.path.dirname(rawPath.replace("\\","/"))        
        if (path and not os.path.exists(path)):
            print('Creo la directory %s.' , (path))
            os.makedirs(path)