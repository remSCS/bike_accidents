# The goal of this project is to create a dynamic dashboard and vizualiation tool in order to explore the data and answer questions about the data.
# The data is from the bike accidents that have occured in France from 2005 to 2018.
# The data is from the following website: https://www.data.gouv.fr/fr/datasets/accidents-corporels-de-la-circulation-routiere/
# We are going to be playing the role of a data analyst for an insurance company that is trying to create a new insurance plan for bike riders.
# The data indicates the circumstances of the accident, the location, the severity of the accident, and the number of people involved.
# It does not indicate the damage to the bike. Therefore, we will be using the data to create a new insurance plan that will cover the cost of the human damage.

import streamlit as st
import pandas as pd
from lib import viz
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(layout="wide",
                   page_title="Bike Accident Dashboard")

@st.cache
def import_data(path):
    return pd.read_csv(path, sep=",")
    
clean = import_data(r'data/clean.csv')
filtered_df = clean.copy()

st.title("Bike Accidents Dashboard")

# Create a topbar where you can navigate to different pages
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Basic Statistics", "Advanced Statistics", "Use case"])

if page == "Basic Statistics":
    st.header("Basic Statistics")   
    # ----- Vizualization -----
    # Plot the map of the accidents
    st.plotly_chart(viz.plot_accidents_map(filtered_df, 1500, 800))
    
    cols = st.columns(2)
    with cols[0]:
        # Plot the histogram of the ages
        st.pyplot(viz.plot_ages_hist(filtered_df))

    with cols[1]:
        # Plot the histogram of the usages
        st.pyplot(viz.plot_usages_hist(filtered_df))
        
    cols = st.columns(3)
    with cols[0]:
        # Plot the histogrma of the severities with contexte
        st.pyplot(viz.plot_hour_line(filtered_df))
    
    with cols[1]:
        # Plot the histogram of the severities with usages
        st.pyplot(viz.plot_day_line(filtered_df))
    
    with cols[2]:
        # Plot the evolution of the accidents over time
        st.pyplot(viz.plot_year_area(filtered_df), height=100)

    # ----- End of vizualization -----

# Create a second page where you can explore the data
if page == "Advanced Statistics":
    # ----- Filters -----
    # st.sidebar.title("Filters")

    # st.sidebar.subheader("Filter by date / time")
    # hour = st.sidebar.slider("Hour", int(clean['heure'].min()), int(clean['heure'].max()), int(clean['heure'].min()))

    # st.sidebar.subheader("Filter by severity")
    # severite = st.sidebar.selectbox("Severity", clean['gravite accident'].unique())

    # filtered_df = viz.filter_data(clean, hour, severite, 'M', [0, 100])
    # ----- End of filters -----
    
    
    # ----- Apply filters -----
    # st.write(df_to_disp.astype(str))
    # ----- End of apply filters -----
    cols = st.columns(2)
    with cols[0]:
        # Plot the histogram of the meteorological conditions
        st.pyplot(viz.plot_meteo_hist(filtered_df))       
    
    with cols[1]:
        # Plot the histogram of the equipments impact on the accidents
        st.pyplot(viz.plot_equipement_impact(filtered_df))
    
    cols = st.columns(2)
    with cols[0]:
        # Plot the histogrma of the severities with contexte
        st.pyplot(viz.plot_severity_usage_hist(filtered_df))
    
    with cols[1]:
        # Plot the histogram of the severities with usages
        st.pyplot(viz.plot_severity_manuever_hist(filtered_df))
        
if page == "Use case":
    st.write("This is the use case page. We are going to focus on the accidents in Paris.")
        
    # Select for the gravity of the accident    
    gravity = st.multiselect("Select the gravity of the accident", filtered_df['gravite accident'].unique(), default=filtered_df['gravite accident'].unique())
    
    # Filter for the travel type
    motive = st.multiselect("Select the motive of the travel", filtered_df['motif deplacement'].unique(), default=filtered_df['motif deplacement'].unique())
    
    # Double slider for the year
    year = st.slider("Select the year", int(filtered_df['annee'].min()), int(filtered_df['annee'].max()), (int(filtered_df['annee'].min()), int(filtered_df['annee'].max())))
    
    # Double slider for the month
    month = st.slider("Select the month", int(filtered_df['num_mois'].min()), int(filtered_df['num_mois'].max()), (int(filtered_df['num_mois'].min()), int(filtered_df['num_mois'].max())))
    
    # Double slider for the day
    day = st.slider("Select the day", int(filtered_df['num_jour'].min()), int(filtered_df['num_jour'].max()), (int(filtered_df['num_jour'].min()), int(filtered_df['num_jour'].max())))
    
    # Double slider for the hour
    hour = st.slider("Select the hour", int(filtered_df['heure'].min()), int(filtered_df['heure'].max()), (int(filtered_df['heure'].min()), int(filtered_df['heure'].max())))
    
    with st.spinner("Loading Map..."):
        st_folium(viz.plot_paris_heatmap(filtered_df, year, month, day, hour, gravity, motive), width=1500, height=800)
    
    st.write("We can see that the accidents are concentrated in the center of Paris. We can also see that the accidents are more frequent in the morning and in the evening, at peak hours.")