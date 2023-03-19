#/usr/bin/python

import getopt
import os
import zimbra
import datetime

class main:
    config = None
    mailboxes = None
    rootdir = None 

    def __init__(self):
        self.rootdir = os.path.dirname(__file__)
        zfs = zimbra.filesystem()
        self.config = zfs.getJsonFile(self.rootdir + '/config.json')
        self.mailboxes = zfs.getJsonFile(self.rootdir + '/mailboxes.json')        
        self.command = self.grabCommand()

    def alignDailyDirectoriesAction(self):        
        zbk = zimbra.DailyReAlign(self.config);
        zbk.exec(self.mailboxes)
    
    def montlyBackupAction(self):
        date = datetime.datetime.strptime('2023-02-01', '%Y-%m-%d')        
        zbk = zimbra.Montly(self.config)
        zbk.exec(self.mailboxes, date)
    
    def yearlyBackupAction(self):
        date = datetime.datetime.strptime('2022-12-31', '%Y-%m-%d')        
        zbk = zimbra.Yearly(self.config)
        zbk.exec(self.mailboxes, date)

    def grabCommand(self):
        return 'syncdays'
    
if (__name__ == "__main__"):
    main().yearlyBackupAction()