import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


dataframe = pd.read_csv('S2BISURVEY.csv', sep=";")

columns_to_be_deleted= ["start", "end", "_insert your GPS location_precision", "select your type of asset",
                        "Use the camera to take a photo or select picture in your phone",
                        "Use the camera to take a photo or select picture in your phone_URL",
                        "comments","insert other ","Use the camera to take a photo or select picture in your phone.1",
                        "Use the camera to take a photo or select picture in your phone_URL.1",
                        "comments.1","Use the camera to take a photo or select picture in your phone.2",
                        "Use the camera to take a photo or select picture in your phone_URL.2","comments.2",
                        "Use the camera to take a photo or select picture in your phone.3",
                        "Use the camera to take a photo or select picture in your phone_URL.3",
                        "comments.3","Use the camera to take a photo or select picture in your phone.4",
                        "Use the camera to take a photo or select picture in your phone_URL.4","comments.4",
                        "Insert other sign panel ","Use the camera to take a photo or select picture in your phone.5",
                        
                        "Use the camera to take a photo or select picture in your phone_URL.5","comments.5",
                        "Use the camera to take a photo or select picture in your phone.7",
                        "Use the camera to take a photo or select picture in your phone_URL.7",
                        "comments.7","Use the camera to take a photo or select picture in your phone.8",
                        "Use the camera to take a photo or select picture in your phone_URL.8","comments.8",
                        "Use the camera to take a photo or select picture in your phone.9",
                        "Use the camera to take a photo or select picture in your phone_URL.9","comments.9",
                        "Field Worker","insert your name","Date","_id","_uuid","_submission_time",
                        "_validation_status","_notes","insert your GPS location","_insert your GPS location_altitude",
                       "_status", "_submitted_by","_tags", "_index",
                       "Use the camera to take a photo or select picture in your phone.6",
                       "Use the camera to take a photo or select picture in your phone_URL.6", "comments.6"]

dataset = dataframe.drop(columns=columns_to_be_deleted,axis=1)
# New school dataset

selected_columns = ['_insert your GPS location_latitude','_insert your GPS location_longitude',
                     'Giving the condition of Schools', 
                    'network coverage around the school ', 'type of school',
                    'School Category', 'select your zone in Douala V']
dataset_school = dataset.loc[:, selected_columns]
# Specify the columns to be considered for deleting missing values
columns_to_check = ['_insert your GPS location_latitude','_insert your GPS location_longitude',
                     'Giving the condition of Schools', 
                    'network coverage around the school ', 'type of school',
                    'School Category', 'select your zone in Douala V']
# Define the minimum number of non-missing values required to retain a line
min_non_missing_values = 6
dataset_school_cleaned = dataset_school.dropna(subset=columns_to_check, thresh=min_non_missing_values)
dataset_school_cleaned['network coverage around the school '] = dataset_school_cleaned['network coverage around the school '].fillna(value='3G')

# Streamlit app
st.title('School Survey Dashboard')

# Sidebar for variable selection
selected_zone = st.sidebar.selectbox('Select Zone in Douala V', dataset_school_cleaned['select your zone in Douala V'].unique())
filtered_data = dataset_school_cleaned[dataset_school_cleaned['select your zone in Douala V'] == selected_zone]

# Display selected variable information
st.write(f"Selected Zone: {selected_zone}")
st.write(f"Number of Schools in {selected_zone}: {len(filtered_data)}")

# Visualization - Condition of Schools
st.header('Condition of Schools')
fig_condition = px.bar(filtered_data, x='Giving the condition of Schools', title='Condition of Schools')
st.plotly_chart(fig_condition)

# Visualization - Type of School
st.header('Type of School')
fig_type = px.pie(filtered_data, names='type of school', title='Distribution of School Types')
st.plotly_chart(fig_type)

# Visualization - School Category
st.header('School Category')
fig_category = px.bar(filtered_data, x='School Category', title='School Category Distribution')
st.plotly_chart(fig_category)

# Visualization - Network Coverage
st.header('Network Coverage around the School')
fig_network = px.pie(filtered_data, names='network coverage around the school ',
                    title='Distribution of Network Coverage')
st.plotly_chart(fig_network)

def plot_school_map(data):
    fig_map = go.Figure()

    # Scatter map plot
    fig_map.add_trace(go.Scattermapbox(
        lat=data['_insert your GPS location_latitude'],
        lon=data['_insert your GPS location_longitude'],
        mode='markers',
        marker=dict(size=10, color='blue'),
        text=data['type of school'],
    ))

    # Layout settings for the map
    fig_map.update_layout(
        mapbox=dict(
            center=dict(lat=data['_insert your GPS location_latitude'].mean(),
                        lon=data['_insert your GPS location_longitude'].mean()),
            style="open-street-map",
            zoom=10,
        ),
    )

    return fig_map

# Visualization - School Map
st.header('School Map')
fig_map = plot_school_map(filtered_data)
st.plotly_chart(fig_map)
