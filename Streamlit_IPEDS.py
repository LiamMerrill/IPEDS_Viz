import streamlit as st
import pandas as pd
import plotly.express as px

# Load data function
@st.cache

def load_data():
    # Replace 'raw.githubusercontent.com' with 'raw.githubusercontent.com/<username>/<repository>/<branch>'
    data_url = 'https://github.com/LiamMerrill/IPEDS_Viz/blob/master/df6.csv'
    data = pd.read_csv(data_url)
    return data
data = load_data()
def main():
    st.title('Exploring IPEDS Data')
    st.write('This is an app that allows for the exploration of select IPEDS data. There are two views, one is a scatter plot and one is a map. For the scatter plot, select continuous variables for X, Y, and then select something like Institution as Displayed Variable to plot. For map.')

    # Load the data
    data = load_data()

    # Create a sidebar for selecting the view mode
    view_mode = st.sidebar.radio('Select View Mode:', ('Plot', 'Map'))

    if view_mode == 'Plot':
        # Create a sidebar for selecting X, Y, and Displayed Variable
        st.sidebar.subheader('Select X and Y Variables')
        x_axis = st.sidebar.selectbox('X-axis:', data.columns, index=data.columns.get_loc('Retention Rate'))
        y_axis = st.sidebar.selectbox('Y-axis:', data.columns, index=data.columns.get_loc('Total digital/electronic circulations (books and media)'))

        st.sidebar.subheader('Select Displayed Variable')
        displayed_variable = st.sidebar.selectbox('Displayed Variable:', data.columns, index=data.columns.get_loc('Institution'))

        # Create a sidebar for selecting color variable
        st.sidebar.subheader('Select Color Variable')
        color_variable = st.sidebar.selectbox('Color Variable:', data.columns, index=data.columns.get_loc('Carnegie Classification 2010: Basic'))

        # Create a sidebar for selecting the year filter
        st.sidebar.subheader('Select Year Filter')
        year_filter = st.sidebar.selectbox('Select Year:', sorted(data['Year'].unique(), reverse=True))

        # Filter data based on the selected year
        filtered_data = data[data['Year'] == year_filter]

        # Scatter plot with ring markers and plasma color scale
        st.subheader('Scatter Plot')
        scatter_fig = px.scatter(
            filtered_data, x=x_axis, y=y_axis, title='Scatter Plot',
            labels={x_axis: 'X-axis', y_axis: 'Y-axis', displayed_variable: 'Displayed Variable'},
            hover_data=[displayed_variable],
            color=color_variable,  # Color based on the selected variable
            color_continuous_scale='plasma'  # Use the plasma color scale
        )
        scatter_fig.update_traces(
            marker=dict(symbol='circle-open', size=10, line=dict(width=2, color='white')),  # Use ring markers
            selector=dict(mode='markers+text', textposition='top center')
        )
        st.plotly_chart(scatter_fig)
    else:
        # Map view
        st.sidebar.subheader('Map View Filters')

        # Create a sidebar for selecting the variable for filtering
        st.sidebar.subheader('Select Filter Variable')
        filter_variable = st.sidebar.selectbox('Filter Variable:', data.columns)

        # Create a sidebar for dynamic filtering of values
        st.sidebar.subheader('Select Filter Values')
        selected_values = st.sidebar.multiselect('Select Values:', data[filter_variable].unique())

        # Apply filters
        if not selected_values:
            filtered_map_data = data
        else:
            filtered_map_data = data[data[filter_variable].isin(selected_values)]

        # Create a sidebar for selecting the variable to represent the size of the dots on the map
        st.sidebar.subheader('Select Size Variable for Map Dots')
        size_variable = st.sidebar.selectbox('Size Variable:', data.columns)

        # Handle NaN values in size_variable
        default_size = 10  # Set a default size for NaN values
        filtered_map_data[size_variable] = filtered_map_data[size_variable].fillna(default_size)

        # Map view with animation
        st.subheader('Map View (Animated)')
        map_fig = px.scatter_geo(
            filtered_map_data, lat='LAT', lon='LON', title='Map View (Animated)',
            labels={'LAT': 'LAT', 'LON': 'LON', 'text': 'Institution'},
            animation_frame='Year',  # Animate based on the "Year" variable
            hover_name='Institution',  # Hover text displays "Institution (entity) name"
            size=size_variable  # Size of the dots based on the selected variable
        )
        st.plotly_chart(map_fig)

if __name__ == "__main__":
    main()
