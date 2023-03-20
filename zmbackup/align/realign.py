from zmbackup.align.align import align
import zmbackup.filesystem
import zmbackup.constant as const

class realign(align):    
    
    def __init__(self, config) -> None:
        super().__init__(config)        

    def exec(self, mailboxes):        
        subDirToAlign = zmbackup.zmbackup.filesystem().getZeroSizeSubDirectory(self.config[const.BACKUP_ROOTDIR_KEY]) 
        self._validateInput(mailboxes, subDirToAlign)
        self._execBackup(mailboxes, subDirToAlign)
    
    def _execBackup(self, mailboxes, subDirToAlign):
        for subDirDate in subDirToAlign:
            for mailbox in mailboxes:
                self.backupper.exec(mailbox, subDirDate)
                self.restorer.exec(mailbox, subDirDate)