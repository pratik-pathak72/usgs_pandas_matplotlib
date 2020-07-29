import pandas as pd
import requests
from sys import argv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

script, site_no = argv

def webpage_to_text(site_no):
    gage_data_url = f'https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb&site_no={site_no}&referred_module=sw&period=&begin_date=1928-06-24&end_date=2020-07-06'
    gage_data = requests.get(gage_data_url)
    gage_data_text = gage_data.text
    return gage_data_text

def parse_gage():
    gage_text = webpage_to_text(site_no)
    gage_text_lines = gage_text.split('\n')
    new_line =[]
    for line in gage_text_lines:
        if '#' not in line and not line.isspace():
            new_line.append(line)
    new_line_str = '\n'.join(new_line)
    with open ('stn_data.txt', 'w') as out_f:
         out_f.write(new_line_str)
    return ''

def to_pandas_df():
    df = pd.read_csv("stn_data.txt",delimiter="\t")
    df = df.drop(df.index[0])
    df = df.loc[:,('datetime', '159218_00060_00003')]
    df = df.rename(columns={"datetime": "Date", "159218_00060_00003": "DailyStreamflow"})
    df["DailyStreamflow"] = df["DailyStreamflow"].astype(float)
    df_sorted = df.sort_values(["DailyStreamflow"],ascending = True)
    return df,df_sorted

def to_matplotlib_plot():
    df,df_sorted = to_pandas_df()
    fig,ax1 = plt.subplots()
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.yaxis.set_major_locator(plt.MaxNLocator(6))
    plt.plot(df.Date,df.DailyStreamflow)
    ax1.set_title(f'Rating Curve for {site_no}')
    plt.show()
    plt.savefig(f'Rating Curve for {site_no}')

def main(site_no):
    parse_gage()
    to_matplotlib_plot()

if __name__ == '__main__':
    main(site_no)
