#libraries to import
import pandas as pd
import time

# convert string type variables to timestamp type
def toTimeStamp(dfcolumnName):
  emptyList = []
  for stamp in dfcolumnName:
    assert isinstance(stamp, object)
    ts = pd.to_datetime(stamp)
    emptyList.append(ts.round(freq='S')) # 'S' means round to nearest second

  return emptyList

#check that the start and end date are the same as now
def checkDate(start, end, now):
  if ((now == start) and (now == end)):
    return True
  else:
    return False

#check that the start and end date are the same as now
def checkDateCase(start, end, now):
  if ((now == start) and (now != end)):
    return True
  else:
    return False

#check that the start and end time are the same as now
def checkTime(start, end, now):
    is_between = False

    is_between |= start <= now <= end
    is_between |= end < start and (start <= now or now <= end)

    return is_between


def convert(time_string):
  time_var = time.strptime(time_string, '%I:%M%p')

  return time_var


#append weather data to the emissions data if conditions are met
def newWeatherData(wLength, eLength, wdate, wtime, edate, etime, wdf, edf):
  newlst = []
  for dt_e in range(eLength - 1):
    #set the weather counters to 0 and 1.
    wCounter1 = 0
    wCounter2 = 1

    for dt_w in range(wLength - 1):
      #start with date and time of weather index 0 and 1
      index1 = dt_w + wCounter1
      index2 = dt_w + wCounter2

      #get the start and end dates
      dateW1 = wdate[index1]
      dateW2 = wdate[index2]

      #get the start and end times
      timeW1 = wtime[index1]
      timeW2 = wtime[index2]
      # print(timeW1, timeW2)

      #increment through the emissions date data
      dateE = edate[dt_e]

      #increment through the emissions date data
      timeE = etime[dt_e]

      if (checkDate(dateW1, dateW2, dateE) == True) and (checkTime(timeW1, timeW2, timeE) == True):
        # print(dateW1, dateW2, dateE, "   ", timeW1, timeW2, timeE, "   ", index1, dt_e)
        #we want information from weather dataframe to fill for each in emissions dataframe
        #extract the row at the index where the conditions are met
        #index of row we want to take data from
        rowIndexW = index1
        rowIndexE = dt_e

        #percent complete
        float = ((dt_e/eLength) * 100)
        format_float = "{:.2f}".format(float)
        print(format_float, '%')
        # extract the row from the dataframe and
        # change extracted row into a list
        extractedRowW = list(wdf.loc[rowIndexW])
        extractedRowE = list(edf.loc[rowIndexE])
        allExtracted = extractedRowE + extractedRowW

        newlst.append(allExtracted)

      elif (checkDateCase(dateW1, dateW2, dateE) == True) and (checkTime(timeW1, timeW2, timeE) == True):
        rowIndexW = index1
        rowIndexE = dt_e

        #percent complete
        float = ((dt_e/eLength) * 100)
        format_float = "{:.2f}".format(float)
        print(format_float, '%')
        # extract the row from the dataframe and
        # change extracted row into a list
        extractedRowW = list(wdf.loc[rowIndexW])
        extractedRowE = list(edf.loc[rowIndexE])
        allExtracted = extractedRowE + extractedRowW

        newlst.append(allExtracted)
        # print(newlst)

  return newlst