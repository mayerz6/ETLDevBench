from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file,"a") as f:
        f.write(timestamp + ',' + message + '\n')

def extract(url, table_attribs):
    ''' This function aims to extract the required information 
    from the website and save it to a dataframe. The function
    returns the dataframe for further processing.
    '''
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('table', {'class': 'wikitable'})
    target_table = tables[0]  # safer than tbody[1]
    rows = target_table.find_all('tr')

    for row in rows[1:]:
        col = row.find_all('td')
        if len(col)>=3:
            data_dict = {"Rank": col[0].contents[0].replace('\n', ''),
                        # "Bank Name": col[1].contents[0],
                        "Market Cap.": col[2].contents[0].replace('\n', '')}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)

    
    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''

    df = pd.read_csv('./exchange_rate.csv')
    currency_dict = dict(zip(df['Currency'], df['Rate']))

    GDP_list = df["Market Cap."].tolist()
    df['MC_GBP_Billion'] = [np.round(x*currency_dict['GBP'],2) for x in GDP_list]
    GDP_list = [float("".join(x.split(','))) for x in GDP_list]
    GDP_list = [np.round(x/1000,2) for x in GDP_list]
    df["GDP_GBP_Billions"] = GDP_list
    # df=df.rename(columns = {"GDP_USD_millions":"GDP_USD_billions"})
    return df
    


url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ["Rank", "Market Cap."]
log_file = './code_log.txt'

log_progress("ETL Job Started")

log_progress("Extract phase Started")
extracted_data = extract(url, table_attribs)
import pandas as pd

df = pd.read_csv('./exchange_rate.csv')
currency_dict = dict(zip(df['Currency'], df['Rate']))
print(currency_dict)

log_progress("Extract phase Ended")

log_progress("Transform phase Started")

transformed_data = transform(extracted_data)
print("Transformed Data")
print(extracted_data)
print(transformed_data)
