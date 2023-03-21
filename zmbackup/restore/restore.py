import requests, os
from os import listdir
import zmbackup.constant

class restore:
    config = None

    def __init__(self, config) -> None:
        self.config = config

    def exec(self, dirName):
        print('Ripristino %s' % (dirName))
        dirPath = os.path.join(self.config[zmbackup.constant.BACKUP_ROOTDIR_KEY], dirName)
        files = listdir(dirPath)
        for filename in files:
            self.upload(os.path.join(dirPath, filename))

    def upload(self, fileName):
        mailboxId = self._extractMailboxIdFromFilename(fileName)
        url = self._urlFactory(mailboxId)
        self._execUpload(url, fileName)
    
    def _extractMailboxIdFromFilename(self, filePath):
        fileName = os.path.basename(filePath)
        return fileName.replace('.tgz','')

    def _urlFactory(self, mailboxId):
        return "https://%s:7071/home/%s/?fmt=tgz&resolve=skip}" % (self.getDestinationHost(), mailboxId)
    
    def _execUpload(self, url, fileName):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',}        
        requests.post(url, headers=headers, data=fileName, verify=False, auth=tuple(self.config['destination']['admin-account']))

    def getDestinationHost(self):
        return self.config['destination']['host']
