from zmbackup.backup.base import base

class daily(base):
    
    def __init__(self, config) -> None:
        self.config = config

    def _getTitle(self, day):
        return 'backup del giorno %s/%s/%s' % (day.day, day.month, day.year)    
            
    def _getDateStartEndPeriod(self, day):
        return (day, day)
        
    def _subDirNameFactory(self, day):
        return "%s-%02d-%02d" % (day.year, day.month, day.day)
    
    def _zimbraApiPeriodUrlFactory(self, host, mailboxId, period):
        strDate = "%02d/%02d/%s" % (period[0].month, period[0].day, period[0].year)
        return "https://%s:7071/home/%s/?fmt=tgz&query=date:%s" % (host, mailboxId, strDate)
        
    def _queryDateFactory(self, day):
        return "%02d/%02d/%s" % (day.month, day.day, day.year)