# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
import datetime

def create_rents_over_time(df):
    df['datetime'] = pd.to_datetime(df['datetime'])
    monthly_df = df.resample('M', on='datetime').sum()
    return monthly_df

#Fungsi untuk menggabungkan penyewaan sepeda berdasarkan data cuaca
def by_weather(df):
    weather_agg = df.groupby("weather_condition").agg({
        "instant": "nunique",
        "count": ["max", "min"]
    })
    return weather_agg

#Fungsi untuk menggabungkan penyewaan sepeda berdasarkan data musim
def by_season(df):
    season_agg = df.groupby("season").agg({
        "instant": "nunique",
        "count": ["max", "min"]
    })
    return season_agg

#Fungsi untuk menggabungkan penyewaan sepeda berdasarkan data harian
def by_day(df):
    weekday_agg = df.groupby("weekday").agg({
        "instant": "nunique",
        "count": ["max", "min"]
    })
    return weekday_agg

#Fungsi untuk menggabungkan persewaan sepeda berdasarkan data bulan
def by_month(df):
    monthly_agg = df.groupby("month").agg({
        "instant": "nunique",
        "count": ["max", "min"]
    })
    return monthly_agg

#Load CSV files
main_df = pd.read_csv("dashboard/data_clean.csv")
datetime_columns = ["datetime"]
main_df.sort_values(by="datetime", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

with st.sidebar:
    st.image("./dashboard/logo.png")

st.header("Dashboard Bike Sharing :bike:")

st.subheader('Daily Rent')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = main_df['casual'].sum()
    st.metric('Casual', value=f'{daily_rent_casual:,}')

with col2:
    daily_rent_registered = main_df['registered'].sum()
    st.metric('Registered', value=f'{daily_rent_registered:,}')

with col3:
    daily_rent_total = main_df['count'].sum()
    st.metric('Total order', value=f'{daily_rent_total:,}')

#Create Dataframes
rents_over_time_df = create_rents_over_time(main_df)
byweather_df = by_weather(main_df)
byseason_df = by_season(main_df)
bymonth_df = by_month(main_df)
byday_df = by_day(main_df)

#Visualisasi Penyewaan Sepeda Seiring Waktu 
st.subheader("Bike Sharing Over Time")
plt.figure(figsize=(10, 6))
plt.plot(rents_over_time_df.index, rents_over_time_df['count'], color='#A5C0DD')
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Bike Sharing Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader('Bike Sharing by Weather Condition')
plt.figure(figsize=(10, 6))
x = byweather_df.index
y_max = byweather_df[('count', 'max')]
y_min = byweather_df[('count', 'min')]
plt.bar(x, y_max, label='Max Sharings', color='#6C9BCF')
plt.bar(x, y_min, label='Min Sharings', color='#A5C0DD')
weather_labels = ['Clear to partly cloudy', 'Light snow to light rain', 'Misty cloudy to misty']
plt.xticks(x, weather_labels)
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Maximum & Minimum Bike Sharing by Weather Condition')
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Musim
st.subheader('Bike Sharing by Season')
plt.figure(figsize=(10, 6))
x = byseason_df.index
y_max = byseason_df[('count', 'max')]
y_min = byseason_df[('count', 'min')]
plt.bar(x, y_max, label='Max Sharings', color='#6C9BCF')
plt.bar(x, y_min, label='Min Sharings', color='#A5C0DD')
season_labels = ['Fall', 'Springer', 'Summer', 'Winter']
plt.xticks(x, season_labels)
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Maximum & Minimum Bike Sharing by Season')
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Hari
st.subheader('Bike Sharing by Weekday')
plt.figure(figsize=(10, 6))
x = byday_df.index
y_max = byday_df[('count', 'max')]
y_min = byday_df[('count', 'min')]
plt.bar(x, y_max, label='Max Sharings', color='#6C9BCF')
plt.bar(x, y_min, label='Min Sharings', color='#A5C0DD')
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Maximum & Minimum Bike Sharing by Weekday')
month_labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
plt.xticks(x,month_labels)
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

#Visualisasi Penyewaan Sepeda Berdasarkan Bulan
st.subheader("Bike Sharing by Month")
plt.figure(figsize=(10, 6))
x = bymonth_df.index
y_max = bymonth_df[('count', 'max')]
y_min = bymonth_df[('count', 'min')]
plt.bar(x, y_max, label='Max Sharings', color='#6C9BCF')
plt.bar(x, y_min, label='Min Sharings', color='#A5C0DD')
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Maximum & Minimum Bike Sharing by Month')
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(x,month_labels)
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

year_copyright = datetime.date.today().year
copyright_dashboard = f"Copyright © {year_copyright} All Rights Reserved [Fannisa Tiara Salsabila](https://www.linkedin.com/in/fannisa-tiara-salsabila-901048231/)"
st.caption(copyright_dashboard)