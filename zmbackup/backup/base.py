import requests, os, json
import datetime
import zmbackup.filesystem
import zmbackup.constant

class base:
    config = None
    mailboxes = None

    def __init__(self, config) -> None:
        self.config = config            

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
        zmbackup.zmbackup.filesystem().saveFile(filePath, fileContent)

    def backupFilenameFactory(self, subDirectory, fileName):
        return os.path.join(self.getOriginHost(), subDirectory, "%s.tgz" % (fileName))
    
    def getOriginHost(self):
        return self.config[zmbackup.zmbackup.constant.BACKUP_ROOTDIR_KEY]
    
    def getOriginAdminAccount(self):
        return tuple(self.config['origin'][zmbackup.zmbackup.constant.ADMIN_ACCOUNT_KEY])