"""
Screen scrape https://cloud.google.com/compute/pricing to get google pricing
adapted from  https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/master/doc/ntbk/z2jh/cost.py
"""
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup as bs4
import locale
#import warnings
#warnings.filterwarnings('ignore')
locale.setlocale(locale.LC_ALL, '')

# --- MACHINE COSTS ---
resp = requests.get('https://cloud.google.com/compute/pricing')
html = bs4(resp.text,"lxml")

# Munge the cost data
def clean_promo(in_value, use_promo=False):
    # cleans listings with promotional pricing
    # defaults to non-promo pricing with use_promo
    if in_value.find("promo") > -1:
        if use_promo:
            return re.search("\d+\.\d+", in_value)[0]
        else:
            return re.search("\d+\.\d+", in_value[in_value.find("("):])[0]
    else:
        return in_value

all_dfs = []
for table in html.find_all('table'):
    header = table.find('thead').find_all('th')
    header = [item.text for item in header]

    data = table.find('tbody').find_all('tr')
    rows = []
    for ii in data:
        thisrow = []
        for jj in ii.find_all('td'):
            if 'default' in jj.attrs.keys():
                thisrow.append(jj.attrs['default'])
            elif 'ore-hourly' in jj.attrs.keys():
                thisrow.append(clean_promo(jj.attrs['ore-hourly'].strip('$')))
            elif 'ore-monthly' in jj.attrs.keys():
                thisrow.append(clean_promo(jj.attrs['ore-monthly'].strip('$')))
            else:
                thisrow.append(jj.text.strip())
        rows.append(thisrow)
    df = pd.DataFrame(rows[:-1], columns=header)
    all_dfs.append(df)


# Pull out our reference dataframes
disk_df = [df for df in all_dfs if 'Price (per GB / month)' in df.columns][0]

machines_list = pd.concat([df for df in all_dfs if 'Machine type' in df.columns]).dropna()
machines_list = machines_list.drop('Preemptible price (USD)', axis=1)
machine_df = machines_list.rename(columns={'Price (USD)': 'Price (USD / hr)'})
# Base costs, all per day
disk_df['Price (per GB / month)'] = disk_df['Price (per GB / month)'].astype(float)

