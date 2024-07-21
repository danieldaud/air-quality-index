import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
import os

def get_day_from_date(year, month, date):
    datetime_format = datetime.datetime(year,month,date)
    day_name = datetime_format.strftime("%A")
    return day_name

st.write("""
# Visualisasi data Air Quality
""")

current_folder = os.path.abspath(os.curdir)

path_data = os.path.join(current_folder,"Air Quality")
path_data_preprocess = os.path.join(current_folder,"preproccessing/data.csv")

progress_text = "Load The Data..."
mybar = st.progress(0, text=progress_text)
try:
    df = pd.read_csv(path_data_preprocess)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date_hour'] = pd.to_datetime(df['date_hour'], format='%Y-%m-%d %H:%M:%S')
    df['year_month'] = pd.to_datetime(df['year_month'], format='%Y-%m')
    
except:
    percent_complete = 0
    df = pd.DataFrame()
    for data in os.listdir(path_data):
        if data.endswith(".csv"):
            df1 = pd.read_csv(os.path.join(path_data,data))
            df = pd.concat([df,df1],axis=0,ignore_index=True)
        percent_complete += int(50/len(os.listdir(path_data)))
        mybar.progress(percent_complete, text=progress_text)
    
    df['hari'] = df.apply(lambda x: get_day_from_date(x[1], x[2], x[3]),axis = 1)
    percent_complete += int(50/4)
    mybar.progress(percent_complete, text="Added Day Column!")
    df['date'] = df.apply(lambda x: datetime.datetime(x[1], x[2], x[3]), axis = 1)
    percent_complete += int(50/4)
    mybar.progress(percent_complete, text="Added Date Column!")
    df['date_hour'] = df.apply(lambda x: datetime.datetime(x[1], x[2], x[3], x[4]), axis = 1)
    percent_complete += int(50/4)
    mybar.progress(percent_complete, text="Added Date with Hour Column!")
    df['year_month'] = df.apply(lambda x: datetime.datetime(x[1], x[2], 1).strftime('%Y-%m'), axis = 1)
    df = df.drop("No",axis=1)
    percent_complete += int(50/4)
    mybar.progress(percent_complete, text="Added Year Month Column!")
    df.to_csv(path_data_preprocess,index=False)
mybar.empty()

data_area = list(df["station"].unique())
# Cleaning data
## Plot Missing Value

st.write('Data yang dimiliki mempunyai nilai kosong, seperti di bawah ini :')
column_name = list(df.columns)
count_missing_values = list(df.isna().sum())
count_data = list(df.isna().count())
percentage_mising_values = [[column_name[i],round(count_missing_values[i]/count_data[i] * 100, 2)] for i in range(len(count_data))]
percentage_mising_values_df = pd.DataFrame(percentage_mising_values,columns=["Column Name","Percetage Missing Data"])
st.bar_chart(percentage_mising_values_df,x="Column Name",y="Percetage Missing Data")


st.write("Data yang kosong akan diisikan dengan nilai hari sebelumnya sesuai areanya masing-masing")
for area in data_area:
    df.loc[df['station'] == area] = df.loc[df['station'] == area].fillna(method='ffill')

new_df = pd.DataFrame()
for area in data_area:
    df1 = df.loc[df['station']==area][24:]
    new_df = pd.concat([new_df,df1],axis=0,ignore_index=True)
new_df.reset_index(drop=True, inplace=True)


# Visualisasi Data

st.sidebar.header("Filter Visualisasi")

area = st.sidebar.selectbox('Area',data_area)
filtered_area = new_df.loc[new_df['station'] == area].reset_index(drop=True)

st.write(f"Data yang tersedia adalah **{filtered_area.loc[0,'date']} - {filtered_area.loc[len(filtered_area)-1,'date']}**")
date_input_start = np.datetime64(st.sidebar.date_input("Start Date", datetime.datetime(filtered_area.loc[0,'year'], filtered_area.loc[0,'month'], filtered_area.loc[0,'day'])))
date_input_end = np.datetime64(st.sidebar.date_input("End Date", datetime.datetime(filtered_area.loc[0,'year'], filtered_area.loc[0,'month'], filtered_area.loc[0,'day'])))

filtered = filtered_area.loc[filtered_area['date']>=date_input_start].reset_index(drop=True)
filtered = filtered.loc[filtered['date']<=date_input_end].reset_index(drop=True)


# PLOT LINE CHART
temp_per_day = filtered.groupby(['date']).mean(numeric_only=True).reset_index()
temp_per_month = filtered.groupby(['year_month']).mean(numeric_only=True).reset_index()

st.write("# Visualisasi PM2.5")
y_axis = "PM2.5"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi PM10")
y_axis = "PM10"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi SO2")
y_axis = "SO2"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi NO2")
y_axis = "NO2"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi CO")
y_axis = "CO"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi O3")
y_axis = "O3"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")

st.write("# Visualisasi rain")
y_axis = "RAIN"
fig1 = px.line(filtered, x="date_hour", y=y_axis)
fig2 = px.line(temp_per_day, x="date", y=y_axis)
fig3 = px.line(temp_per_month, x="year_month", y=y_axis)
pos = st.tabs(["By Hour", "By Day", "By Month"])
pos[0].plotly_chart(fig1, theme="streamlit")
pos[1].plotly_chart(fig2, theme="streamlit")
pos[2].plotly_chart(fig3, theme="streamlit")