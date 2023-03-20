from zmbackup.backup.base import base as baseBackup
import zmbackup.filesystem
import zmbackup.zmbackup.constant
import calendar

class montly(baseBackup):    
    
    def __init__(self, config) -> None:
        self.config = config

    def exec(self, mailboxes, month):
        self._validateInput(mailboxes, month)
        self._execBackup(mailboxes, month)
        
    def _validateInput(self, mailboxesToBackup, month):
        if not mailboxesToBackup:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not month:
            raise Exception('Non hai passato un mese valido da backuppare')

    def _execBackup(self, mailboxes, day):
        period = self._getDateStartEnd(day)
        subDir = self._subDirNameFactory(day)
        hostOrigin = self.getOriginHost()
        adminAccount = self.getOriginAdminAccount()
        for mailboxId in mailboxes:                
            url = super()._zimbraApiPeriodUrlFactory(hostOrigin, mailboxId, period)
            localFilename = self.backupFilenameFactory(subDir, mailboxId)
            zmbackup.zmbackup.filesystem().downloadAndSaveBackupFile(url, localFilename, adminAccount)
    
    def _getDateStartEnd(self, day):
        daysOfMonth = calendar.monthrange(day.year, day.month)[1]
        dateStart = day.replace(day=1)        
        dateEnd = day.replace(day=daysOfMonth)
        return (dateStart, dateEnd)

    def _subDirNameFactory(self, day):
        return "%s-%02d" % (day.year,day.month)