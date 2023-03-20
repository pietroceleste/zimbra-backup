from zmbackup.backup.daily import dailyBackup
from zmbackup.restore.restore import restore
import zmbackup.filesystem
from datetime import datetime,date, timedelta

class align:    
    backupper = None
    restorer = None

    def __init__(self, config) -> None:
        self.config = config
        self.backupper = dailyBackup(self.config)
        self.restorer = restore(self.config)

    def exec(self, fromDate, mailboxes):        
        self._validateInput(mailboxes, fromDate)
        self._execBackup(fromDate, mailboxes)
        
    def _validateInput(self, mailboxesToBackup, fromDate):
        if not mailboxesToBackup:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not fromDate:
            raise Exception('Non hai fornito una data di partenza per l\'allineamento')

    def _execBackup(self, fromDate, mailboxes):
        cur_date = datetime.strptime(fromDate, '%Y-%m-%d')
        end_date = datetime.today()
        delta = timedelta(days=1)
        while cur_date <= end_date:            
            for mailbox in mailboxes:
                self.backupper.exec(date, mailbox)
                self.restorer.exec(date, mailbox)
            cur_date += delta
