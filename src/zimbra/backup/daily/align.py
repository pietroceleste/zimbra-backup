from zimbra.backup.base import base
import zimbra.filesystem

class align(base):    
    
    def __init__(self, config) -> None:
        self.config = config

    def exec(self, mailboxes):
        subDirToAlign = zimbra.filesystem().getZeroSizeSubDirectory(self.config['backupRootDir'])
        self._validateInput(mailboxes, subDirToAlign)
        self._execBackup(mailboxes, subDirToAlign)
        
    def _validateInput(self, mailboxesToBackup, subDirToAlign):
        if not mailboxesToBackup:
            raise Exception('Non ci sono caselle di posta da allineare')
        if not subDirToAlign:
            raise Exception('Non giorni da allineare')

    def _execBackup(self, mailboxes, subDirToAlign):
        for date in subDirToAlign:
            for mailbox in mailboxes:
                response = super()._getBakupFromOirigin(mailbox, date)
                self.saveBackupFile(date, mailbox, response.content)                
