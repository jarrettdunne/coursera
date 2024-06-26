# Import required libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = set(spacex_df['Launch Site'])
launch_site_options = [{'label': j, 'value': j} for i, j in enumerate(launch_sites)]
launch_site_options.insert(0, {'label': 'All Sites', 'value': 'ALL'})

outcome = {0: 'Failure', 1: 'Success'}
spacex_df['MissionOutcome'] = spacex_df['class'].replace(outcome)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=launch_site_options,
                                    value='ALL',
                                    # placeholder='select launch site',
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                # marks={
                                                #     0: '0',
                                                #     100: '100'
                                                #     },
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(value):
    filtered_df = spacex_df[spacex_df['Launch Site'] == value]
    if value == 'ALL':
        fig = px.pie(spacex_df[spacex_df['class'] == 1], values='class', 
        names='Launch Site', 
        title='Total Successful Launches By Site')
        fig.update_traces(textinfo='value')
        return fig
    else:
        pass
        # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, 
        names='MissionOutcome', 
        title=f'Launch Outcome Percentages for site {value}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(value1, value2):
    filtered_df = spacex_df[spacex_df['Launch Site'] == value1]

    slider_df = spacex_df[spacex_df['Payload Mass (kg)'].between(value2[0], value2[1])]
    
    site_slider_df = filtered_df[filtered_df['Payload Mass (kg)'].between(value2[0], value2[1])]
    
    if value1 == 'ALL':
        fig = px.scatter(slider_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",

        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        fig = px.scatter(site_slider_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",

        title=f'Correlation between Payload and Success for site {value1}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
