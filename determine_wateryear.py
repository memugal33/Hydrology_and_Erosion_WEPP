from datetime import datetime, timedelta, date


#### This code takes the julian day and year as an input and gives back...
#### ...water year as an output
def determine_wateryear(y, j=None, mo=None):
    '''
    This codes assumes that Julian day starts from 0
    If the Julian day starts from 1, put J-1 while calling the function
    '''
    
    if j is not None:
        mo = int((datetime(int(y), 1, 1) + timedelta(int(j))).month)
        day = int((datetime(int(y), 1, 1) + timedelta(int(j))).day)
    if mo > 9:
        return [y + 1,mo,day]

    return [y,mo,day]
