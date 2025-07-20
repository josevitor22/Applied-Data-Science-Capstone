# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex dataset into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get max and min payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Task 1: Create an app layout with a dropdown for launch sites, a pie chart, a slider, and a scatter chart
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Dropdown for Launch Site
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # Task 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    # Task 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Task 2: Add a callback function for `success-pie-chart`
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success vs Failure for site {entered_site}'
        )
    return fig

# Task 4: Add a callback function for `success-payload-scatter-chart`
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_plot(site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title='Success by Payload Mass for All Sites'
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)', y='class',
            color='Booster Version Category',
            title=f'Success by Payload Mass for site {site}'
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
