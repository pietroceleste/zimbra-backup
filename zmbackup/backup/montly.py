from zmbackup.backup.base import base as baseBackup
from zmbackup.backup.download import download as backupDownload
import calendar

class montly(baseBackup):    
    
    def __init__(self, config) -> None:
        self.config = config

    def _getTitle(self, day):
        return 'backup del mese %s/%s' % (day.month, day.year)    
    
    def _getDateStartEndPeriod(self, day):
        daysOfMonth = calendar.monthrange(day.year, day.month)[1]
        dateStart = day.replace(day=1)        
        dateEnd = day.replace(day=daysOfMonth)
        return (dateStart, dateEnd)

    def _subDirNameFactory(self, day):
        return "%s-%02d" % (day.year,day.month)
