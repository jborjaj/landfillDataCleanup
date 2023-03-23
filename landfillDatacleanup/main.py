import datafunctions
import pandas as pd

# # *************************************************************************************************
#Import raw data
weatherDF = pd.read_csv(r'C:\Users\JBorja\PycharmProjects\pythonProject\Weather_ 2020-2022_TequesquiteLandfill.csv')
emissionsDF = pd.read_csv(r'C:\Users\JBorja\PycharmProjects\pythonProject\Emissions_2020-2022_TequesquiteLandfill.csv')

# # *************************************************************************************************
#clean the weather data
#remove weather data columns not needed for analysis
weatherDF = weatherDF.drop(['name', 'preciptype', 'snow', 'snowdepth', 'feelslike', \
                                   'windgust', 'solarenergy', 'uvindex', 'severerisk', 'precipprob', \
                             'icon', 'stations'], axis=1)

#rename the header (columns)
weatherDF.columns = ["datetime_weather_str", "tempF", "dew", "humidity", "precip", \
                       "windspeed", "winddir","sealevelpressure", "cloudcover", "visibility", \
                        "solarradiation", "conditions"]

#convert datetime weather to timestamp
ts_w_List = datafunctions.toTimeStamp(weatherDF.datetime_weather_str)

#add the new list to the dataframe as a column
weatherDF['datetime_weather_ts'] = ts_w_List
# weatherDF.assign(datetime_weather_new = ts_w_List)

# create seperate columns for date and time
weatherDF["weatherDate"] = weatherDF["datetime_weather_ts"].dt.date
weatherDF["weatherTime"] = weatherDF["datetime_weather_ts"].dt.time

# organize the dataframe by date in ascending order
weatherDF.sort_values(by='datetime_weather_ts', ascending=True)
# # *************************************************************************************************
#clean the emissions data
#rename the header (columns)
emissionsDF.columns = ["datetime_emissions_str", "CH4_percent", "CO2_percent", "O2_percent", \
                       "remainder_percent", "internalPressure_Hg", "FAUtemp_degF", "flowMain_SCFM"]


var = emissionsDF.datetime_emissions_str
#convert datetime emissions to timestamp
ts_e_List = datafunctions.toTimeStamp(var)

#add the new list to the dataframe as a column
emissionsDF['datetime_emissions_ts'] = ts_e_List

#remove all rows if there is a zero in flowMain_SCFM
emissionsDF = emissionsDF[emissionsDF['flowMain_SCFM'] != 0]

# organize the dataframe by date in ascending order
emissionsDF = emissionsDF.sort_values(by='datetime_emissions_ts', ascending=True)

#reset the indeces since we removed the zero values in rows
emissionsDF = emissionsDF.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')

#remove columns not needed for analysis
emissionsDF = emissionsDF.drop(['index'], axis=1)

# create seperate columns for date and time
emissionsDF["emissionsDate"] = emissionsDF["datetime_emissions_ts"].dt.date
emissionsDF["emissionsTime"] = emissionsDF["datetime_emissions_ts"].dt.time

# # *************************************************************************************************
#arguments for the newWeatherFata function
emissionLength = len(weatherDF.weatherDate)
weatherLength = len(emissionsDF.emissionsDate)
wdate = weatherDF.weatherDate
wtime = weatherDF.weatherTime
edate = emissionsDF.emissionsDate
etime = emissionsDF.emissionsTime

newList = datafunctions.newWeatherData(emissionLength, weatherLength, wdate, wtime, edate, etime, weatherDF, emissionsDF)
# print(newList)
# convert the list to DataFrame
data = pd.DataFrame(newList)

# save as a CSV file
data.to_csv('landfillDataNEW1.csv', sep =',')