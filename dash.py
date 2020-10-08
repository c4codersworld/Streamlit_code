import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import requests
import datetime


    
  
page_bg_img = '''
<style>
body {
background-image: url("https://mipa.unram.ac.id/wp-content/uploads/2019/09/Savin-NY-Website-Background-Web.jpg");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)



state_total = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
state_data  = state_total.json()
sdata = pd.DataFrame.from_dict(state_data['data']['regional']) 
sdata = sdata.rename(columns = {'loc': 'State','discharged': 'Recovered','deaths': 'Deaths','totalConfirmed': 'Confirmed'}, inplace = False)
sdata['State'][31] = 'Telangana'
state_sort_data = sdata.sort_values(by=['Confirmed'], ascending=False)

Country_timeline =requests.get('https://api.covid19india.org/data.json')
Country_timeline = Country_timeline.json()
country_data = pd.DataFrame.from_dict(Country_timeline['cases_time_series']) 
country_data = country_data.rename(columns = {'dailyconfirmed': 'Daily Confirmed','dailydeceased': 'Daily Deaths','dailyrecovered': 'Daily Recovered','date': 'Date'}, inplace = False)
country_data_timeline = country_data[['Daily Confirmed', 'Daily Deaths','Daily Recovered','Date']]

start_date = datetime.date(2020, 1, 30)
number_of_days = len(country_data['Date'])

date_list = []
for day in range(number_of_days):
    a_date = (start_date + datetime.timedelta(days = day)).isoformat()
    date_list.append(a_date)


country_data_timeline['Dates'] = date_list





#st.title("Covid-19 Dashboard For India")
st.markdown("<h1 style='text-align: left; color: red;'>Covid-19 Dashboard For India</h1>",unsafe_allow_html=True)
st.markdown('The dashboard visualizes the Covid-19 condition in India')

#st.markdown('Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.')
st.sidebar.title("Visualization Selector")



bar_select = st.sidebar.selectbox('Most COVID States', ['All', 'Confirmed','Recovered','Deaths'], key='1')



if bar_select=='All':
    st.markdown("<h3 style='text-align: left; color: blue;'>Most COVID States</h1>",unsafe_allow_html=True)
    fig = go.Figure(data=[
    go.Bar(name='Confirmed', x=state_sort_data['State'][:5], y=state_sort_data['Confirmed'][:5]),
    go.Bar(name='Recovered', x=state_sort_data['State'][:5], y=state_sort_data['Recovered'][:5]),
    go.Bar(name='Deaths', x=state_sort_data['State'][:5], y=state_sort_data['Deaths'][:5])])
    st.plotly_chart(fig)

if bar_select=='Confirmed':
    st.markdown("<h3 style='text-align: left; color: blue;'>Most COVID States</h1>",unsafe_allow_html=True)
    fig = go.Figure(data=[
    go.Bar(name='Confirmed', x=state_sort_data['State'][:5], y=state_sort_data['Confirmed'][:5])])
    st.plotly_chart(fig)

if bar_select=='Recovered':
    st.markdown("<h3 style='text-align: left; color: blue;'>Most COVID States</h1>",unsafe_allow_html=True)
    state_sort_data = sdata.sort_values(by=['Recovered'], ascending=False)
    fig = go.Figure(data=[
    go.Bar(name='Recovered', x=state_sort_data['State'][:5], y=state_sort_data['Recovered'][:5])])
    st.plotly_chart(fig)

if bar_select=='Deaths':
    st.markdown("<h3 style='text-align: left; color: blue;'>Most COVID States</h1>",unsafe_allow_html=True)
    state_sort_data = sdata.sort_values(by=['Deaths'], ascending=False)
    fig = go.Figure(data=[
    go.Bar(name='Deaths', x=state_sort_data['State'][:5], y=state_sort_data['Deaths'][:5])])
    st.plotly_chart(fig)


line_select = st.sidebar.selectbox('Daily Confirmed, Recovered Cases , Daily Deaths', ['All', 'Confirmed','Recovered','Deaths'])


if line_select == 'All':
    st.markdown("<h3 style='text-align: left; color: blue;'>Daily Confirmed, Recovered Cases , Daily Deaths</h1>",unsafe_allow_html=True)
    fig = px.line(country_data_timeline, x="Date", y=["Daily Confirmed","Daily Recovered","Daily Deaths"])
    st.plotly_chart(fig)


if line_select == 'Confirmed':
    st.markdown("<h3 style='text-align: left; color: blue;'>Daily Confirmed</h1>",unsafe_allow_html=True)
    fig = px.line(country_data_timeline, x="Date", y=["Daily Confirmed"])
    st.plotly_chart(fig)

if line_select == 'Recovered':
    st.markdown("<h3 style='text-align: left; color: blue;'>Daily Confirmed</h1>",unsafe_allow_html=True)
    fig = px.line(country_data_timeline, x="Date", y=["Daily Recovered"])
    st.plotly_chart(fig)

if line_select == 'Deaths':
    st.markdown("<h3 style='text-align: left; color: blue;'>Daily Deaths</h1>",unsafe_allow_html=True)
    fig = px.line(country_data_timeline, x="Date", y=["Daily Deaths"])
    st.plotly_chart(fig)

st.markdown("<h3 style='text-align: left; color: blue;'>COVID Spread In India</h1>",unsafe_allow_html=True)
st_data  = sdata[['State','Confirmed']]
fig = px.choropleth(
    st_data,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Confirmed',
    color_continuous_scale='Reds'
)

fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)
