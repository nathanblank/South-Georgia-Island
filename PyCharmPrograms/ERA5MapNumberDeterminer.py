import datetime
import numpy as np
from datetime import date, timedelta, datetime
human_year = 0.
human_month = 0.
human_day = 0.
human_hour = 0.
#human_year = int(input('Input year: '))
#human_month = int(input('Input month: '))
#human_day = int(input('Input day: '))
#human_hour = int(input('Input hour (interval of 6 and between 0 - 24): '))
human_year = 2001
human_month = 1
human_day = 1
human_hour = 0

time_difference = datetime(human_year,human_month,human_day,human_hour,0,0) - datetime(1900, 1, 1,0,0,0)
print(time_difference)

hoursSinceTrueStart = time_difference*24
print(hoursSinceTrueStart)

#print(daysChange)
newDTBegin = timedelta(np.float64(0 / 24.))

print(newDTBegin)

