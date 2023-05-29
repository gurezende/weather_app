# Imports
import pandas as pd
import streamlit as st
from datetime import datetime
from meteostat import Point, Monthly

# Set Page Layout
st.set_page_config(layout='wide')

#-----------------------------------------------------------------------
# Load the Dataset
cities = pd.read_csv('world_cities.csv')

#-----------------------------------------------------------------------

# Select box
st.subheader('Temperature History App')

col1, col2 = st.columns(2, gap='medium')
# column 1 - Table weather history
with col1:
    # Title of the select box
    selected_city = st.selectbox(label='Select a city for weather information',
                                 options=cities['city'].sort_values().unique())

with col2:
    selected_year = st.selectbox(label= 'Select an year',
                                 options= range(2022,1999,-1) )


#-----------------------------------------------------------------------
# Collect the Weather Information
# Set time period
start = datetime(selected_year, 1, 1)
end = datetime(selected_year, 12, 31)

# Create Point
lat = cities.query('city == @selected_city')['latitude'].astype('float').tolist()[0]
long = cities.query('city == @selected_city')['longitude'].astype('float').tolist()[0]
city_loc = Point(lat, long)

# Get daily data for 2018
data = Monthly(city_loc, start, end)
data = data.fetch()
#data['mth'] = data.index.month
data = data[ ['tavg', 'tmax', 'tmin'] ]

col1, col2 = st.columns(2, gap='large')
# column 1 - Table weather history
with col1:
    st.text('| TEMPERATURES IN °C')
    st.line_chart(data=data)

# column 2 - Graphics
with col2:
    # WEATHER INFORMATION TABLE
    st.text('| WEATHER HISTORY')
    st.write(data)


#-----------------------------------------------------------------------

# Division
st.markdown('---')
# Map
st.subheader('| WHERE THIS CITY IS')
df_map = cities.query('city == @selected_city')
st.map(df_map, zoom=5)


