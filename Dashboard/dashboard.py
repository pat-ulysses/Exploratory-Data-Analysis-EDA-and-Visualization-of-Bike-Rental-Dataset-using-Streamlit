import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Get the current directory
current_directory = os.path.dirname(__file__)

# Load the dataset using a relative path
data = pd.read_csv(os.path.join(current_directory, "bike_data.csv"))

def casual_sum(df):
    return df['casual_hour'].sum()

def registered_sum(df):
    return df['registered_hour'].sum()

def by_season_sum(df):
    by_season_sum_df=df.groupby('season_hour')['cnt_hour'].sum().sort_values(ascending=True)
    return by_season_sum_df

def by_weather_sum(df):
    by_weather_sum_df=df.groupby('weathersit_hour')['cnt_hour'].sum().sort_values(ascending=True)
    return by_weather_sum_df

# Sidebar
with st.sidebar:
    #Filters
    plot_type = st.sidebar.selectbox("Select Plot Type", ["Senin", "Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"])
if plot_type=='Senin':
    temp=1
elif plot_type=='Selasa':
    temp=2
elif plot_type=='Rabu':
    temp=3
elif plot_type=='Kamis':
    temp=4
elif plot_type=='Jumat':
    temp=5
elif plot_type=='Sabtu':
    temp=6
else :
    temp=0

main_df=data[(data['weekday_day'])==temp]

# Main content
st.title("Bike Sharing Dataset Dashboard :sparkles: ")

st.subheader('Rentals by Day')
 
col1, col2, col3= st.columns(3)
 
with col1:
    total_casual = casual_sum(main_df)
    st.metric("Total casual renters", value=total_casual)
 
with col2:
    total_registered = registered_sum(main_df)
    st.metric("Total registered renters", value=total_registered)

with col3:
    total_renters = registered_sum(main_df) + casual_sum(main_df)
    st.metric("Total renters", value=total_renters)

#Barplot
x=['number of casual users','number of registered users']
y=[casual_sum(main_df),registered_sum(main_df)]

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(x,y,color="#90CAF9")
ax.set_title('Number of registered vs casual users')
ax.set_ylabel('Number of rentals (in tens of millions)')
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

#Number of bike rentals by the hour
st.subheader("Bike Rentals by the hour")

fig, ax = plt.subplots(figsize=(35, 15))
sns.pointplot(x='hr', y='cnt_day', data=main_df)
ax.set_ylabel('Amount of rentals')
ax.set_title("Rentals by the hour", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(35, 15))
sns.boxplot(x='hr', y='cnt_day', data=main_df)
ax.set_ylabel('Amount of rentals')
ax.set_title("Rentals by the hour", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# By weather and season
st.subheader("Rentals by Weather and Season")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

#1
temp_df=pd.DataFrame(by_season_sum(main_df))
sns.barplot(x="season_hour", y="cnt_hour", data=temp_df, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Season", fontsize=30)
ax[0].set_title("Rentals by season", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

#2
temp_df=pd.DataFrame(by_weather_sum(main_df))
sns.barplot(x="weathersit_hour", y="cnt_hour", data=temp_df, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Weather", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Rentals by Weather", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
