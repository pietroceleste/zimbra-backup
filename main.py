#/usr/bin/python

import getopt
import os
import zmbackup
from datetime import datetime

class main:
    config = None
    mailboxes = None
    rootdir = None 

    def __init__(self):
        self.rootdir = os.path.dirname(__file__)
        zfs = zmbackup.filesystem()
        self.config = zfs.getJsonFile(self.rootdir + '/conf/config.json')
        self.mailboxes = zfs.getJsonFile(self.rootdir + '/conf/mailboxes.json')        
        self.command = self.grabCommand()

    def restoreTodayFactory(self):
        rst = zmbackup.restore(self.config)
        rst.exec('2023-03-21')

    def alignDailyDirectoriesAction(self):        
        zbk = zmbackup.DailyAlign(self.config);
        zbk.exec(self.mailboxes, datetime.strptime('2023-03-01', '%Y-%m-%d'))
    
    def dailyBackupAction(self):        
        zbk = zmbackup.Daily(self.config)
        zbk.exec(self.mailboxes, datetime.today())

    def montlyBackupAction(self):        
        zbk = zmbackup.Montly(self.config)
        zbk.exec(self.mailboxes, datetime.strptime('2023-03-01', '%Y-%m-%d'))
    
    def yearlyBackupAction(self):        
        zbk = zmbackup.Yearly(self.config)
        zbk.exec(self.mailboxes, datetime.strptime('2022-12-31', '%Y-%m-%d'))

    def grabCommand(self):
        return 'syncdays'
    
if (__name__ == "__main__"):
    main().restoreTodayFactory()