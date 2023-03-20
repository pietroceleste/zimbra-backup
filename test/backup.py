import unittest
import os
from src.zimbra.filesystem import filesystem as zfs
from src.zimbra.backup.daily import daily

class TestBackup(unittest.TestCase):
    config = None
    rootdir = None
    mailboxes = None

    def initConfig(self):
        zfs = zfs()
        self.rootdir = os.path.dirname(__file__) + '/../src'
        self.config = zfs.getJsonFile(self.rootdir + '/config.json')
        self.mailboxes = zfs.getJsonFile(self.rootdir + '/mailboxes.json')    

    def test_backup_daily(self):
        bk = daily(self.config)

if __name__ == '__main__':
    unittest.main()