from zimbra.backup.daily.align import align
import zimbra.filesystem
import zimbra.constant as const

class realign(align):    
    
    def __init__(self, config) -> None:
        self.config = config        

    def exec(self, mailboxes):        
        subDirToAlign = zimbra.filesystem().getSubDirectory(self.config[const.ROOTDIRKEY])    
        self._validateInput(mailboxes, subDirToAlign)
        self._execBackup(mailboxes, subDirToAlign)            