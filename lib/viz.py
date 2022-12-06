# This script will be dedicated to the creation of the vizualization tools.
# It will be used to create the graphs and charts that will be used in the dashboard.
# The graphs and charts will be created using matplotlib, seaborn, and plotly.
# The goal is to allow them to be dynamic and interactive.
 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import folium
from folium.plugins import HeatMap

def filter_data(df, hour_range, severite, sex, age_range):
    fil = df[df['heure'] >= hour_range[0]]
    fil = fil[fil['heure'] <= hour_range[1]]
    fil = fil[fil['gravite accident'] == severite]
    fil = fil[fil['sexe'] == sex]
    fil = fil[fil['age'] >= age_range[0]]
    fil = fil[fil['age'] <= age_range[1]]
    return fil

# Create a function that will create a map of the accidents
def plot_accidents_map(df, w, h):
    # Center the map on France
    center = {"lat": 46.2276, "lon": 2.2137}
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", 
                            color="gravite accident", 
                            hover_name="gravite accident", 
                            hover_data=["gravite accident", "motif deplacement", "age"], 
                            zoom=5, height=h, width=w,
                            center=center)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

# Create a function that will create a bar chart of the number of accidents by age group
def plot_ages_hist(df):
    ages = [i for i in range(0, 106, 5)]
    labels = [f"{i}-{i+4}" for i in range(0, 104, 5)]
    df['age group'] = pd.cut(df['age'], ages, labels=labels)
    fig, ax = plt.subplots(figsize=(10, 6))
    # Bar plot with ordered ages
    ax = df['age group'].value_counts().sort_index().plot(kind='bar', color='blue')
    ax.set_xlabel("Age group")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by age group")
    return ax.figure

# Create a function that will create a bar chart of the number of accidents by usage
def plot_usages_hist(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Bar plot with ordered ages
    ax = df['motif deplacement'].value_counts().plot(kind='bar', color='blue')
    ax.set_xlabel("Usage")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by usage")
    return ax.figure

# Create a function that will create a stacked bar charts of the number of accidents by meteorological conditions and severity using plotly
def plot_meteo_hist(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df.groupby(['conditions atmosperiques', 'gravite accident'])['gravite accident'].count().unstack('gravite accident').plot(kind='bar', stacked=True)
    ax.set_xlabel("Meteorological conditions")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by meteorological conditions and severity")
    return ax.figure

# Create a function that will create a horizontal stacked bar charts of the number of accidents by severity and usage using plotly
def plot_severity_usage_hist(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df.groupby(['motif deplacement', 'gravite accident'])['gravite accident'].count().unstack('gravite accident').plot(kind='barh', stacked=True)
    ax.set_xlabel("Number of accidents")
    ax.set_ylabel("Usage")
    ax.set_title("Number of accidents by usage and severity")
    return ax.figure

# Create a function that will create a horizontal stacked bar charts of the number of accidents by severrity and manuever using plotly
def plot_severity_manuever_hist(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df.groupby(['manoeuvre avant accident', 'gravite accident'])['gravite accident'].count().unstack('gravite accident').plot(kind='barh', stacked=True)
    ax.set_xlabel("Number of accidents")
    ax.set_ylabel("Manuever")
    ax.set_title("Number of accidents by usage and severity")
    return ax.figure

# Create a function that will generate a line chart of the number of accidents by hour
def plot_hour_line(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df['heure'].value_counts().sort_index().plot(kind='line', color='blue')
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by hour")
    return ax.figure

# Create a function that will generate a line chart of the number of accidents by day
def plot_day_line(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df['jour'].value_counts().sort_index().plot(kind='line', color='blue')
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by day")
    return ax.figure

# Create a functoin that will generate an area chart of the number of accidents by year and color code the severity
def plot_year_area(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df.groupby(['annee', 'gravite accident'])['gravite accident'].count().unstack('gravite accident').plot(kind='area')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by year and severity")
    # Add a small legend at the top right
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=6)
    return ax.figure

# Create a functoin that will generate a graph reprensenting the impact of equipement on the severity of accidents
def plot_equipement_impact(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax = df.groupby(['existence securite', 'gravite accident'])['gravite accident'].count().unstack('gravite accident').plot(kind='bar')
    ax.set_xlabel("Equipement")
    ax.set_ylabel("Number of accidents")
    ax.set_title("Number of accidents by equipement and severity")
    return ax.figure

# Plot a geographical map with a heatmap over it of the number of accidents with a range slider for the year, month, day and hour
def plot_paris_heatmap(df, year_range, month_range, day_range, hour_range, gravity, motive):
    # Filter the dataframe by the year range
    df = df[(df['annee'] >= year_range[0]) & (df['annee'] <= year_range[1])]
    # Filter the dataframe by the month range
    df = df[(df['num_mois'] >= month_range[0]) & (df['num_mois'] <= month_range[1])]
    # Filter the dataframe by the day range
    df = df[(df['num_jour'] >= day_range[0]) & (df['num_jour'] <= day_range[1])]
    # Filter the dataframe by the hour range
    df = df[(df['heure'] >= hour_range[0]) & (df['heure'] <= hour_range[1])]
    # Filter the dataframe by the gravity (list of severity)
    df = df[df['gravite accident'].isin(gravity)]
    # Filter the dataframe by the motive of the trip (lisd of motives)
    df = df[df['motif deplacement'].isin(motive)]
    
    depts = ["75", "77", "78", "91", "92", "93", "94", "95"]
    paris_df = df[df['departement'].isin(depts)]
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)
    HeatMap(paris_df[['lat', 'lon']].values.tolist(), radius=20).add_to(m)
    return m