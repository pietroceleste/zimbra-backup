import requests, os


class restore:
    config = None

    def __init__(self, config) -> None:
        self.config = config

    def upload(self, fileName):
        mailboxId = self._extractMailboxIdFromFilename(fileName)
        url = self._urlFactory(mailboxId, fileName)
        self._execUpload(url, fileName)
    
    def _extractMailboxIdFromFilename(self, filePath):
        fileName = os.path.basename(filePath)
        return fileName.replace('.tgz','')

    def _urlFactory(self, mailboxId):
        return "https://{self.config['destination']['host']:7071/home/{mailboxId}/?fmt=tgz&resolve=skip}"
    
    def _execUpload(self, url, fileName):
        headers = {'Content-Type': 'application/x-www-form-urlencoded',}        
        requests.post(url, headers=headers, data=fileName, verify=False, auth=tuple(self.config['destination']['admin-account']))
