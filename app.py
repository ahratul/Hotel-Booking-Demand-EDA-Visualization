import warnings
warnings.filterwarnings('ignore')
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
# %matplotlib inline

df = pd.read_csv('hotel_bookings.csv')

df.isnull().sum().sort_values(ascending=False)
# Percentage of missing values by column

round((df.isnull().sum().sort_values(ascending=False) * 100) / len(df), 2)
values = {'company': 0, 'agent': 0}

df.fillna(value=values, inplace=True)

# Replacing NULL values in country column with most frecuent value

df['country'].fillna(value=df['country'].mode()[0], inplace=True)

# Removing row affected by NULL values in children column

df.dropna(subset=['children'], inplace=True)
df.isnull().sum()
cat_columns = ['hotel', 'is_canceled', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest',
               'reserved_room_type', 'assigned_room_type', 'deposit_type', 'customer_type', 'reservation_status']

for cat_column in cat_columns:
    unique_values = df[cat_column].unique()
    print(f"\n{cat_column}: \n{unique_values}\n")
    print('-' * 70)

# Replacing 'undefined' meal with 'SC'

df['meal'].replace(to_replace='Undefined', value='SC', inplace=True)
df['meal'].unique()
df.drop(df[df['adults'] == 0].index, inplace=True)
len(df[df['adults'] == 0])
# Columns from `df.describe()` I want to examine

features = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies',
            'previous_cancellations', 'previous_bookings_not_canceled', 'booking_changes', 'adr',
            'days_in_waiting_list']

# Creating a boxplot and a histogram for outlier detection

n = 1

sns.set_style('darkgrid')
sns.set(font_scale=1.2)
plt.figure(figsize=(16, 28))

for feature in features:
    plt.subplot(15, 2, n)
    sns.boxplot(df[feature], palette='autumn').set(xlabel=None)
    plt.title(f'{feature} boxplot')
    n = n + 1

    plt.subplot(15, 2, n)
    plt.hist(df[feature], color='#f7b267')
    plt.title(f'{feature} histogram')
    n = n + 1
    plt.tight_layout()

features = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies',
            'previous_cancellations', 'previous_bookings_not_canceled', 'booking_changes', 'adr',
            'days_in_waiting_list']

n = 1

sns.set_style('darkgrid')
sns.set(font_scale=1.2)
plt.figure(figsize=(14, 18))

for feature in features:
    plt.subplot(4, 3, n)
    sns.stripplot(x=df['hotel'], y=df[feature], palette='summer').set(xlabel=None, ylabel=None)
    plt.title(f'{feature} strip plot')
    n = n + 1
    plt.tight_layout()

# Number of bookings that have more than 10 previous bookings not canceled for resort

num_high_pb = len(df[(df['previous_bookings_not_canceled'] > 10) & (df['hotel'] == 'Resort Hotel')])

# Number of bookings made by companies that had more than 10 previous bookings not canceled for resort

num_companies_high_pb = len(
    df[(df['previous_bookings_not_canceled'] > 10) & (df['company'] > 0) & (df['hotel'] == 'Resort Hotel')])

# Number of bookings made by private individuals that had more than 10 previous bookings not canceled for resort

num_indiv_high_pb = len(
    df[(df['previous_bookings_not_canceled'] > 10) & (df['company'] == 0) & (df['hotel'] == 'Resort Hotel')])

# percentage of companies and individuals that had more than 10 previous cancellations for the resort

companies_high_pb_percent = round((num_companies_high_pb / num_high_pb) * 100, 2)

indiv_high_pb_percent = round((num_indiv_high_pb / num_high_pb) * 100, 2)

df.loc[df['lead_time'] > 380, ['lead_time']] = 380
df.loc[df['stays_in_weekend_nights'] > 6, ['stays_in_weekend_nights']] = 6
df.loc[df['stays_in_week_nights'] > 10, ['stays_in_week_nights']] = 10
df.loc[df['adults'] > 4, ['adults']] = 4
df.loc[df['children'] > 8, ['lead_time']] = 0
df.loc[df['babies'] > 8, ['babies']] = 0
df.loc[df['booking_changes'] > 5, ['booking_changes']] = 5
df.loc[df['days_in_waiting_list'] > 0, ['days_in_waiting_list']] = 1
df.loc[df['previous_cancellations'] > 0, ['previous_cancellations']] = 1
df.loc[df['previous_bookings_not_canceled'] > 0, ['previous_bookings_not_canceled']] = 1

# Dropping row with extreme outlier in adr column

df.drop(df[df['adr'] == 5400].index, inplace=True)

df.duplicated().sum()

# Dropping duplicate rows

df.drop_duplicates(inplace=True)

df['arrival_date_year'] = df['arrival_date_year'].astype('str')
df['arrival_date_month'] = df['arrival_date_month'].astype('str')
df['arrival_date_day_of_month'] = df['arrival_date_day_of_month'].astype('str')
df['is_repeated_guest'] = df['is_repeated_guest'].astype('str')
df['is_canceled'] = df['is_canceled'].astype('str')
df['previous_cancellations'] = df['previous_cancellations'].astype('str')
df['previous_bookings_not_canceled'] = df['previous_bookings_not_canceled'].astype('str')

df['arrival_date'] = df['arrival_date_day_of_month'] + '-' + df['arrival_date_month'] + '-' + df['arrival_date_year']
df['arrival_date'] = pd.to_datetime(df['arrival_date'], errors='coerce')

df['kids'] = df['children'] + df['babies']
df['total_members'] = df['kids'] + df['adults']

df['total_nights'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']


df['arrival_date_month'] = df['arrival_date'].dt.month

country_visitors = df[df['is_canceled'] == '0'].groupby(['country']).size().reset_index(name='count')


f=px.choropleth(country_visitors,
              locations="country",
              color="count",
              hover_name="country",
              color_continuous_scale="dense",
              projection='orthographic',
              title="Nationality of visitors"
              )

st.write(f)