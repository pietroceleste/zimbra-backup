from zmbackup.backup.montly import montly

class yearly(montly):

    def _getDateStartEnd(self, day):        
        dateStart = day.replace(day=1, month=1)        
        dateEnd = day.replace(day=31, month=12)
        return (dateStart, dateEnd)
    
    def _subDirNameFactory(self, day):
        return str(day.year)
