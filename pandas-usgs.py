import pandas as pd
import requests
from sys import argv
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

script, site_no = argv

def webpage_to_text(site_no):
    gage_data_url = f'https://nwis.waterdata.usgs.gov/nwis/peak?site_no={site_no}&agency_cd=USGS&format=rdb'
    gage_data = requests.get(gage_data_url)
    gage_data_text = gage_data.text
    return gage_data_text

def main(site_no):
    gage_text = webpage_to_text(site_no)
    with open ('stn_data.txt', 'w') as out_f:
         out_f.write(gage_text)

    with open('stn_data.txt', 'r') as f:
        with open('stn_data_edited.txt','w') as f1:
            linelist = f.readlines()
            for line in linelist:
                if '#' not in line and not line.isspace():
                    f1.write(line)

    df = pd.read_csv("stn_data_edited.txt",delimiter="\t")
    df = df.drop(df.index[0])
    df = df.loc[:,('peak_dt', 'peak_va')]
    df['peak_va'] = df['peak_va'].astype(int)
    df_sorted = df.sort_values(['peak_va'],ascending = True)
    print(df)
    fig,ax1 = plt.subplots()
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(6))
    plt.plot(df.peak_dt,df.peak_va)
    ax1.set_title(f'Rating Curve for {site_no}')
    plt.show()
    plt.savefig(f'Rating Curve for {site_no}')

if __name__ == '__main__':
    main(site_no)
