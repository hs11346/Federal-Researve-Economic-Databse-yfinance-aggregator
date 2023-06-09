# Federal-Researve-Economic-Databse-yfinance-aggregator
This code is a wrapper around the Federal Reserve Economic Database (FRED) and yahoo finance (yfinance) API, and merges them based on customisable settings. The function that is used is merge_data.

Data from yfinance include stock prices and index prices, which comes at an array of intervals such as 1m, 1d etc, while FRED data has a fixed interval for different time series data. The function have the option to resample the data to the higest-frequency interval, or just do an outer join and render the missing values as NaN.

An example would be:

df = merge(api='XXXX',\
      start='2021-01-01',\
      end = '2022-12-31',\
      interval='1d',\
      yf_code='^GSPC,^DJI,^IXIC,^STOXX,^FTSE,^VIX',\
      fred_code='WTISPLC,DGS10,PWHEAMTUSDM,BAA10Y,T10Y2Y,AAA,DBAA',\
      resamp_freq='M',\
      resamp_format = 'first')

Parameter list:
API: The API key for the FRED API which is found from the FRED website

Start: the start date of data
End: End date of data, by default it is today's date

Interval: the interval of the yfinance data

yf_code: A string containing no, one or multiple yfinance codes, seperated by a comma. If no yfinance codes are needed, leave it blank (default)

fred_code: Same as yf_code, but for FRED codes

resamp_freq: Upsample the data to match the data frequency of the dataframe (df.resample function, 'H','D','M' etc), default is no

resamp_format: get first or last data of the group, default is last

remove_min: remove the minute timestamp from the datetime index, defalt is yes


