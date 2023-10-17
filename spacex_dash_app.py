import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                        # Task 1:Add a Launch Site Drop-down Input Component
                                dcc.Dropdown(id='site_dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(),

                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                html.Div(dcc.Graph(id='success-pie-chart')),
                html.Br(),

                #Function decorator to specify function input and output
                html.P("Payload range (Kg):"),

                # TASK 3: Add a slider to select payload range
                #dcc.RangeSlider(id='payload-slider',...)
                dcc.RangeSlider(id='payload_slider',
                                 min=0, max=10000, step=1000, marks={0: '0', 1000: '1000', 2000: '2000',
                                                                                   3000: '3000', 4000: '4000', 5000: '5000',
                                                                                   6000: '6000', 7000: '7000', 8000: '8000',
                                                                                   9000: '9000', 10000: '10000'},
                                value=[min_payload, max_payload]),

                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                ])

#TASK 2:
# Add a callback function for 'site-dropdown as input', 'success-pie-chart' as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site_dropdown', component_property='value')
            )
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class',
                     names='Launch Site', 
                     title='Success Launch All sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        filtered_df = filtered_df
        fig = px.pie(filtered_df, 
                     values='class count', 
                     names='class', 
                     title=f"Total Success Launches for site {site_dropdown}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success_payload_scatter_chart', component_property='figure'),
        [Input(component_id='site_dropdown', component_property='value'),
        Input(component_id='payload_slider', component_property='value')])

def get_scatter_plot(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        low_value, high_value=payload_slider
        filtered_scatter_df=spacex_df[(spacex_df['Payload Mass (kg)'] >= low_value) & (spacex_df['Payload Mass (kg)'] <= high_value)]
        fig=px.scatter(filtered_scatter_df, 
                       x='Payload Mass (kg)', 
                       y='class', 
                       color='Booster Version Category',
                       hover_data=['Booster Version'],
                       title='Success Launch for All Sites with Respect to Payload Mass (kg)')
        return fig
    else:
        filtered_scatter_options_df=filtered_scatter_df[filtered_scatter_df['Launch Site'] == site_dropdown]
        fig=px.scatter(filtered_scatter_options_df, 
                       x='Payload Mass (kg)', 
                       y='class',
                       color='Booster Version Category', 
                       hover_data=['Booster Version'],
                       title='Success Launch for' + site_dropdown + 'Site With Respect to Payload Mass (kg)')
        return fig

# Run the app
if __name__ == '__main__':
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
      app.run_server()