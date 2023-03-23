#/usr/bin/python3

import getopt,sys
import os
import zmbackup
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class main:
    config = None
    mailboxes = None
    rootdir = None
    zfs = None 
    argv_manager = None

    def __init__(self):
        self.__init_root_dir__()
        self.__init_zimbra_fs__()
        #try:
        self.__init_argv_manager__()
        self.__init_configuration__()                       
        self.__init_mailboxes_list__()        
        if (not self.argv_manager.execute()):
            self.alignDailyDirectoriesAction(datetime.today())
        #except Exception as ex:
        #    print(ex)

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
        margv.addLong('--align-yesterday', self.alignYesteradyAction, False)
        margv.addLong('--realign', self.alignDailyDirectoriesAction)
        margv.addLong('--backup-dayly', self.dailyBackupAction)
        margv.addLong('--backup-yesterday', self.yesterdayBackupAction, False)
        margv.addLong('--backup-montly', self.montlyBackupAction)
        margv.addLong('--backup-last-month', self.lastMonthBackupAction, False)
        margv.addLong('--backup-yearly', self.yearlyBackupAction)
        margv.addLong('--backup-last-year', self.lastYearBackupAction, False)
        margv.addLong('--debug')
        margv.setHelpMessage('zmbackup.py [--backup-yearly=yyyy-mm-dd] [--backup-last-year] [--backup-montly=yyyy-mm-dd] [--backup-last-month] [--backup-daily=yyyy-mm-dd] [--restore=subfolder]')
        margv.init(sys.argv[1:])
        self.argv_manager = margv            

    def restoreAction(self, subFolder):
        rst = zmbackup.restore(self.config)
        rst.exec(subFolder)

    def alignDailyDirectoriesAction(self, date):        
        zbk = zmbackup.DailyAlign(self.config)
        zbk.exec(self.mailboxes, date)
    
    def alignYesteradyAction(self):        
        day = datetime.today() - timedelta(days=1)        
        self.alignDailyDirectoriesAction(day.strftime('%Y-%m-%d'))

    def dailyBackupAction(self, date):
        zbk = zmbackup.Daily(self.config)
        zbk.exec(self.mailboxes, date)
    
    def yesterdayBackupAction(self):
        day = datetime.today() - timedelta(days=1)        
        self.dailyBackupAction(day.strftime('%Y-%m-%d'))

    def montlyBackupAction(self, date):        
        zbk = zmbackup.Montly(self.config)
        zbk.exec(self.mailboxes, date)
    
    def lastMonthBackupAction(self):
        day = datetime.today() - relativedelta(months=1)
        self.montlyBackupAction(day.strftime('%Y-%m-%d'))
    
    def yearlyBackupAction(self, date):
        zbk = zmbackup.Yearly(self.config)
        zbk.exec(self.mailboxes, date)
    
    def lastYearBackupAction(self):
        day = datetime.today() - relativedelta(years=1)        
        self.yearlyBackupAction(day.strftime('%Y-%m-%d'))
    
if (__name__ == "__main__"):
    main() #.alignDailyDirectoriesAction()