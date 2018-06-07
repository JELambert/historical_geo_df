# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 12:26:22 2018

@author: Jesus
"""

import pandas as pd
import geopandas as gpd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import os
import imageio
from natsort import natsorted
import urllib.request as urllib2
from bs4 import BeautifulSoup



def time_frame(df, time_unit):

    """
    Args:
        df (pandas dataframe)
        time_unit (datetime object)
    Returns:
        A list of ordered unique dates
    """

    df[time_unit] = pd.to_datetime(df[time_unit])
    dates = [date for date in list(pd.unique(df[time_unit]))]
    return dates


def upsample(dates):


    """
    Args:
        dates (List) - List of ordered unique dates
    Returns:
        A list of DataFrames
    """

    filename = 'historical_shape.shp'
    his_date = gpd.read_file(filename)
    today = datetime.date.today()
    his_date = his_date[his_date['ccode'] >=1]
    his_date['date_s'] = pd.to_datetime(his_date['date_s'])
    his_date['date_e'] = pd.to_datetime(his_date['date_e'])
    his_date.loc[his_date.date_e == '2016-06-30 00:00:00', 'date_e'] = today

    pd.options.mode.chained_assignment = None
    df_list = []
    #num = 0
    for i, date in enumerate(dates):

        up = his_date[(his_date['date_s']<= date) & (his_date['date_e']>= date)]
        #his_date = his_date
        up['date'] = date
        up['num'] = i
        df_list.append(up)

    return df_list


def merge_all(df, df_list):

    """
    Args:
        df (pandas dataframe)
        df_list (list) - list of dataframes

    Returns:
        An upsampled dataframe
    """

    df_list = gpd.GeoDataFrame(pd.concat(df_list, ignore_index=False))
    df = df_list.merge(df, on=['ccode', 'date'], how='right')
    return df


def make_poly(df, time_unit):

    """
    Args:
        df (pandas dataframe)
        time_unit (datetime object)

    Returns:
        GeoDataFrame merged
    """
    dates = time_frame(df, time_unit)
    df_list = upsample(dates)

    df = merge_all(df, df_list)
    return df



def collapse(df, unit):

    """
    Args:
        df (pandas dataframe)
        unit (unit to collapse by) - can be 'month' or 'year'

    Returns:
        GeoDataFrame merged
    """

    if unit == "month":
        df['day'] = 1
        df['date']= pd.to_datetime(df['year']*10000+df['month']*100+df['day'],format='%Y%m%d')
        df['government'] = df['government'].astype('category')
        df['regime'] = df['government'].cat.codes
        df = df.sort_values(by=['ccode', 'date', 'pt_attempt'])
        subs = df.drop_duplicates(subset=['ccode', 'date'], keep='last')
        df = subs
        return df

    elif unit == "year":
        df = df[df.month == 1]
        #df = df.groupby(['ccode', 'year'], as_index=False).sum()
        #df = df.set_index(['ccode', 'year']).groupby(level=0, as_index=False).cumsum()
        #df = df.reset_index()
        df['day'] = 1
        #df['month'] = 1
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        df = df.sort_values(by=['ccode', 'date', 'pt_attempt'])
        subs = df.drop_duplicates(subset=['ccode', 'date'], keep='last')
        df = subs
        return df



def get_reign(url):

    """
    Scrape the most up to date Reign Data
    Takes URL of github
    Returns CSV href
    """

    open_url = urllib2.urlopen(url)
    soup = BeautifulSoup(open_url, 'html.parser')
    p_tags = soup.findAll('p')
    href = p_tags[2].find('a')
    reign = href.attrs['href']

    return reign


def main():

    reign = get_reign('https://oefdatascience.github.io/REIGN.github.io/menu/reign_current.html')
    df = pd.read_csv(reign)
    df = collapse(df, 'year')
    named_df = make_poly(df, 'date')


    reign_2018 = named_df[named_df.date == '2018-01-01']
    reign_1970 = named_df[named_df.date == '1970-01-01']

    reign_2018.plot(column='age', legend=True, vmin=20, vmax=90)
    reign_1970.plot(column='age', legend=True, vmin=20, vmax=90)


    """
    Make above maps

    The below commands will make gif, as long as the only .png 's in working folder
    are the maps created.

    """


    """
    image_dir = os.getcwdb()

    print('Creating GIF...')
    image_files = get_image_files(image_dir, '', shortened=0)
    image_list = []
    for f in image_files:
        image = imageio.imread(os.path.join(image_dir, f))
        image_list.append(image)
    imageio.mimsave(os.path.join(image_dir, 'animation' + '.gif'), image_list, format='GIF', duration=1/fps)

    """



    return named_df

if __name__ == '__main__':
    named_df = main()
