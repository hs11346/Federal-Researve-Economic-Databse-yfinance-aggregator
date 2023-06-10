import fredapi as fd
import pandas as pd
import numpy as np
import yfinance as yf
import time
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

#api is the api key from the fredapi library, which is obtained from the FRED website
#start is the starting date of the data
#end is the ending date, by default it is today's date
#interval is the date interval of the yfinance data
#please see the readme file for parameters details
def merge_data(api,start,end=datetime.today().strftime('%Y-%m-%d'),interval='1d',yf_code='na',fred_code='na',resamp_freq = 'no',resamp_format = 'last',remove_min="Y"):
    master_dict = {}
    df = pd.DataFrame()
    fred = fd.Fred(api_key=api)
    first = True
    if yf_code != "na" and fred_code == "na":
        yf_code = yf_code.split(",")
        master_dict = {i:"yfinance" for i in yf_code}
    if yf_code == "na" and fred_code != "na":
        fred_code = fred_code.split(",")
        master_dict = {i:"fred" for i in fred_code}
    if yf_code != "na" and fred_code != "na":
        fred_code = fred_code.split(",")
        yf_code = yf_code.split(",")
        yf_dict = {i:"yfinance" for i in yf_code}
        fred_dict = {i:"fred" for i in fred_code}
        yf_dict.update(fred_dict)
        master_dict = yf_dict
    for code, source in master_dict.items():
        
        if source == "fred":
            temp = fred.get_series(code)            
            
        if source == "yfinance":
            time.sleep(1) # To slow down dowload speed from yfinance, adjustable
            ticker = yf.Ticker(code)
            temp = ticker.history(start=start,end=end,interval=interval)
            
            temp = temp.rename(columns={"Close":code})[code]
        temp.index = pd.to_datetime(temp.index)
        temp = temp[start:end]
        temp.name = code
        if first:
            df = temp
            first = False
        else: 
            df = pd.merge(df,temp,how="outer",left_index=True, right_index=True)      

    if resamp_freq != "no":
        if resamp_format == 'last':
            df = df.resample(resamp_freq,base=1).last()
        elif resamp_format == 'first':
            df = df.resample(resamp_freq,base=1).first()
    if remove_min == "Y":
        df = df.reset_index()
        df = df.rename(columns={"index":"Date"})
        df["Date"] = df["Date"].astype(str)
        df.Date = df.Date.apply(lambda x: x.replace(" 00:00:00",""))
        df = df.set_index("Date")

    return df
            

