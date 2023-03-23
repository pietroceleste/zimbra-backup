from zmbackup.backup.daily import daily as dailyBackup
from zmbackup.restore.restore import restore
from datetime import datetime,date, timedelta

class align:    
    backupper = None
    restorer = None

    def __init__(self, config) -> None:
        self.config = config
        self.backupper = dailyBackup(self.config)
        self.restorer = restore(self.config)

    def exec(self, mailboxes, fromDate):   
        self._validateInput(mailboxes, fromDate)        
        self._execBackup(mailboxes, fromDate)
        
    def _validateInput(self, mailboxes, fromDate):
        if not mailboxes:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not fromDate:
            raise Exception('Non hai fornito una data di partenza per l\'allineamento')
        if isinstance(fromDate, str):
            datetime.strptime(fromDate, '%Y-%m-%d')

    def _execBackup(self, mailboxes, fromDate):
        cur_date = datetime.strptime(fromDate, '%Y-%m-%d')
        end_date = datetime.today()        
        delta = timedelta(days=1)        
        while cur_date <= end_date:                                    
            self.backupper.exec(mailboxes, cur_date)            
            self.restorer.exec('%s-%02d-%02d' % (cur_date.year, cur_date.month, cur_date.day))
            cur_date += delta        
            
