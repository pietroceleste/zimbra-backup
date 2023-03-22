import requests, os, json
import datetime
import zmbackup.filesystem
import zmbackup.constant
from zmbackup.backup.download import download as backupDownload

class base:
    config = None
    mailboxes = None

    def __init__(self, config) -> None:
        self.config = config        
    
    def exec(self, mailboxes, rawDay):
        self._validateInput(mailboxes, rawDay)
        day = rawDay if not isinstance(rawDay, str) else datetime.datetime.strptime(rawDay, '%Y-%m-%d')
        print('Start ' + self._getTitle(day))
        self._execBackup(mailboxes, day)
        print('End ' + self._getTitle(day))    

    def _getTitle(self, day):
        return 'backup base'

    def _validateInput(self, mailboxesToBackup, day):
        if not mailboxesToBackup:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not day:
            raise Exception('Non hai passato un giorno valido da backuppare')
        if isinstance(day, str):
            datetime.datetime.strptime(day, '%Y-%m-%d')
    
    def _execBackup(self, mailboxes, day):
        period = self._getDateStartEndPeriod(day)
        subDir = self._subDirNameFactory(day)
        hostOrigin = self.getOriginHost()
        adminAccount = self.getOriginAdminAccount()
        for mailboxId in mailboxes:            
            url = self._zimbraApiPeriodUrlFactory(hostOrigin, mailboxId, period)
            localFilename = self.backupFilenameFactory(subDir, mailboxId)
            backupDownload().exec(url, adminAccount, localFilename)

    def _getBakupFromOrigin(self, user, rawdate):
        date = datetime.datetime.strptime(rawdate, '%Y-%m-%d').strftime('%m/%d/%y')
        requests.packages.urllib3.disable_warnings()
        url = self._zimbraApiUrlFactory(self.getOriginHost(), user, date)
        print(url)
        return requests.get(url, verify=False,auth=self.getOriginAdminAccount())
    
    def _getPeriodBackupFromOrigin(self, user, period):        
        requests.packages.urllib3.disable_warnings()
        url = self._zimbraApiPeriodUrlFactory(self.config['origin']['host'], user, period)
        return requests.get(url, verify=False, auth=self.getOriginAdminAccount())
    
    def _zimbraApiPeriodUrlFactory(self, host, mailboxId, period):
        dateStart = "%02d/%02d/%s" % (period[0].month, period[0].day, period[0].year)
        dateEnd = "%02d/%02d/%s" % (period[1].month, period[1].day, period[1].year)
        return f"https://{host}:7071/home/{mailboxId}/?fmt=tgz&query=after:\"{dateStart}\"%20and%20before:\"{dateEnd}\""

    def saveBackupFile(self, subDirectory, fileName, fileContent):
        filePath = os.path.join(self.getOriginHost(), subDirectory, "%s.tgz" % (fileName))
        zmbackup.filesystem().saveFile(filePath, fileContent)

    def backupFilenameFactory(self, subDirectory, fileName):
        return os.path.join(self.getBackupRootDirectory(), subDirectory, "%s.tgz" % (fileName))
    
    def getOriginHost(self):
        return self.config[zmbackup.constant.ORIGIN]['host']
    
    def getOriginAdminAccount(self):
        return tuple(self.config['origin'][zmbackup.constant.ADMIN_ACCOUNT_KEY])
    
    def getBackupRootDirectory(self):
        return self.config[zmbackup.constant.BACKUP_ROOTDIR_KEY]