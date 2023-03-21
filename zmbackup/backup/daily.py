from zmbackup.backup.base import base
from zmbackup.backup.download import download as backupDownload
import zmbackup.constant

class daily(base):
    
    def __init__(self, config) -> None:
        self.config = config

    def exec(self, mailboxes, day):
        self._validateInput(mailboxes, day)
        self._execBackup(mailboxes, day)
        
    def _validateInput(self, mailboxesToBackup, day):
        if not mailboxesToBackup:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not day:
            raise Exception('Non hai passato un giorno valido da backuppare')

    def _execBackup(self, mailboxes, day):        
        subDir = self._subDirNameFactory(day)
        hostOrigin = self.getOriginHost()
        adminAccount = self.getOriginAdminAccount()
        strDate = self._queryDateFactory(day)
        for mailboxId in mailboxes:                            
            url = super()._zimbraApiPeriodUrlFactory(hostOrigin, mailboxId, strDate)
            localFilename = self.backupFilenameFactory(subDir, mailboxId)
            backupDownload().exec(url, adminAccount, localFilename)

    def _subDirNameFactory(self, day):
        return "%s-%02d-%02d" % (day.year, day.month, day.day)
    
    def _zimbraApiPeriodUrlFactory(self, host, mailboxId, strDate):
        return "https://%s:7071/home/%s/?fmt=tgz&query=date:%s" % (host, mailboxId, strDate)
        
    def _queryDateFactory(self, day):
        return "%02d/%02d/%s" % (day.month, day.day, day.year)