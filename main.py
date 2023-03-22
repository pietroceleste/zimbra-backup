#/usr/bin/python

import getopt,sys
import os
import zmbackup
from datetime import datetime

class main:
    config = None
    mailboxes = None
    rootdir = None
    zfs = None 
    argv_manager = None

    def __init__(self):
        self.__init_root_dir__()
        self.__init_zimbra_fs__()
        try:
            self.__init_argv_manager__()
            self.__init_configuration__()                       
            self.__init_mailboxes_list__()        
            if (not self.argv_manager.execute()):
                self.alignDailyDirectoriesAction(datetime.today())
        except Exception as ex:
            print(ex)

    def __init_root_dir__(self):
        self.rootdir = os.path.dirname(__file__)

    def __init_zimbra_fs__(self):
        self.zfs = zmbackup.filesystem()

    def __init_configuration__(self):        
        self.config = self.zfs.getJsonFile(
            self.argv_manager.getOption(
                '--config-file',
                self.rootdir + '/conf/config.json'
            )
        )

    def __init_mailboxes_list__(self):        
        self.mailboxes = self.zfs.getJsonFile(
            self.argv_manager.getOption(
                '--mailboxes-file',
                self.rootdir + '/conf/mailboxes.json'
            )
        )

    def __init_argv_manager__(self):
        margv = zmbackup.argv_manager()
        margv.addShort("hs:")
        margv.addLong('--restore', self.restoreAction)
        margv.addLong('--align', self.alignDailyDirectoriesAction)
        margv.addLong('--realign', self.alignDailyDirectoriesAction)
        margv.addLong('--backup-yearly', self.yearlyBackupAction)
        margv.addLong('--backup-montly', self.montlyBackupAction)
        margv.addLong('--backup-dayly', self.dailyBackupAction)        
        margv.addLong('--debug')
        margv.setHelpMessage('zmbackup.py [--backup-yearly=yyyy-mm-dd] [--backup-montly=yyyy-mm-dd] [--backup-daily=yyyy-mm-dd] --restore=subfolder')
        margv.init(sys.argv[1:])
        self.argv_manager = margv            

    def restoreAction(self, subFolder):
        rst = zmbackup.restore(self.config)
        rst.exec(subFolder)

    def alignDailyDirectoriesAction(self, date):        
        zbk = zmbackup.DailyAlign(self.config);
        zbk.exec(self.mailboxes, date)
    
    def dailyBackupAction(self, date):
        zbk = zmbackup.Daily(self.config)
        zbk.exec(self.mailboxes, date)

    def montlyBackupAction(self, date):        
        zbk = zmbackup.Montly(self.config)
        zbk.exec(self.mailboxes, date)
    
    def yearlyBackupAction(self, date):
        zbk = zmbackup.Yearly(self.config)
        zbk.exec(self.mailboxes, date)
    
if (__name__ == "__main__"):
    main() #.alignDailyDirectoriesAction()