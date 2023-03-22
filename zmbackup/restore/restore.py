import requests, os
from os import listdir
import zmbackup.constant

class restore:
    config = None

    def __init__(self, config) -> None:
        self.config = config

    def exec(self, dirName):
        dirPath = os.path.join(self.config[zmbackup.constant.BACKUP_ROOTDIR_KEY], dirName)
        self.validateTargetDirectory(dirPath)
        print('Ripristino %s' % (dirName))        
        files = listdir(dirPath)
        for filename in files:
            self.upload(os.path.join(dirPath, filename))

    def validateTargetDirectory(self,dirName):
        if (not os.path.exists(dirName)):
            raise Exception('La directory %s non esiste. Impossibile procedere con il ripristino del backup' % (dirName))

    def upload(self, fileName):
        mailboxId = self._extractMailboxIdFromFilename(fileName)
        url = self._urlFactory(mailboxId)
        rsp = self._execUpload(url, fileName)
        print(rsp)
    
    def _extractMailboxIdFromFilename(self, filePath):
        fileName = os.path.basename(filePath)
        return fileName.replace('.tgz','')

    def _urlFactory(self, mailboxId):
        return "https://%s:7071/home/%s/?fmt=tgz&resolve=skip" % (self.getDestinationHost(), 'test@qandas.it')
        #return "https://%s:7071/home/%s/?fmt=tgz&resolve=skip" % (self.getDestinationHost(), mailboxId)
    
    def _execUpload(self, url, fileName):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',}        
        requests.packages.urllib3.disable_warnings()
        fileContent = open(fileName, 'rb')        
        return requests.post(url, headers=headers, data=fileContent.read(), verify=False, auth=self.getDestinationAdmin())

    def getDestinationHost(self):
        return self.config['destination']['host']
    
    def getDestinationAdmin(self):
        return tuple(self.config['destination']['admin-account'])
