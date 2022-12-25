import pandas as pd
from pathlib import Path
import re
import sys

if len(sys.argv) == 1:
    print("No file was dropped\n")
    print("please Drag and Drop the file")
    exit()
path = sys.argv[1]
#path = r"C:\Users\MrM\Desktop\gonyu_data_fusion-20221125T125555Z-001\gonyu_data_fusion\moz2.csv"
data = pd.read_csv(path).drop(index=0)
datan = pd.DataFrame()
#assignt it for the first column of the data
datan['Date'] = data[data.columns[0]]
datan[data.columns[1]] = data[data.columns[1]]
datan = datan.drop_duplicates(subset='Date', keep='first')

def get_date_format(date): # get the date format
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return "%Y-%m-%d"
    elif re.match(r"^\d{2}-\d{2}-\d{4}$", date):
        return "%d-%m-%Y"
    elif re.match(r"^\d{2}/\d{2}/\d{4}$", date):
        return "%m/%d/%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{2}$", date):
        return "%Y/%d/%m"
    elif re.match(r"^\d{4}\d{2}\d{2}$", date):
        return "%Y%m%d"
    elif re.match(r"^\d{2}\d{2}\d{4}$", date):
        return "%d%m%Y"
    elif re.match(r"^\d{4}/\d{2}/\d{4}$", date):
        return "%Y/%m/%d"
    elif re.match(r"^\d{2} \w{3} \d{4}$", date):
        return "%d %b %Y"
    elif re.match(r"^\d{2} \w{4,9} \d{4}$", date):
        return "%d %B %Y"
    else:
        return None

def day_interpolation(df): # interpolates the missing values by day
    newdf = df.copy(deep=True)
    try:
        getform = get_date_format(newdf['Date'].iloc[1].astype(str))
        newdf['Date'] = pd.to_datetime(newdf['Date'], format=getform)
    except:
        getform = get_date_format(newdf['Date'].iloc[1])
        newdf['Date'] = pd.to_datetime(newdf['Date'], format=getform)
    else:
        pass
    newdf = newdf.set_index('Date')
    newdf = newdf.resample('D')
    newdf = newdf.interpolate(method='linear')
    newdf = newdf.reset_index()
    return newdf

def get_df_name(df): # get the name of the file
    name = Path(df).stem
    return name

dayinter = pd.DataFrame(day_interpolation(datan))
named = get_df_name(path)
dayinter.to_csv(".\\" + named + "_DayInter.csv", index=False)
'''tff = check_if_equal(intsplit)
tff.reset_index(inplace = True, drop = True)
tff.set_index('x', inplace = True)
autocorrelation_plot(tff['y'])
scaterplot(tff['x'], tff['y'])'''