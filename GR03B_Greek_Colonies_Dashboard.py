import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import webbrowser
import plotly.graph_objects as go
from GR03A_DataFrame import create_df_for_viz,txt_to_dataframe
import dash_table

def create_app():

    # Load dataframe to plot bubble map
    df=create_df_for_viz()
    # list of category for each trace
    category = df['Category'].unique()
    # list of colours to assign to each trace
    colors = ["royalblue","crimson","lightseagreen","orange","limegreen"]

    # Function to generate bubble map figure
    def generate_bubble_map():
        figure = go.Figure()

        for index,value in enumerate(category):
            df_cat = df[df.Category == value ]
            figure.add_trace(go.Scattergeo(
                lon = df_cat.Longitude,
                lat = df_cat.Latitude,
                text = df_cat.Trace_Text,
                marker = dict(
                    size = df_cat['No of Cities']*20,
                    color = colors[index],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode = 'area'
                ),
                name = value))

        figure.update_layout(
            title_text = '<b>Number of Colonies by Location</b> <br>Before Philip II of Macedon (Pre-Hellenic)',
            title_x=0.5,
            showlegend = True,
            width=1050,
            height=1050,
            legend=dict(
                orientation='h'
            ),
            margin=go.layout.Margin(
                b=500
            ),
            geo = dict(
                center=dict(
                    lon=20.2,
                    lat=41.2
                ),
                projection=dict(
                    scale=7
                ),
                showcoastlines=True,
                showcountries=True,
                showframe=False,
                landcolor = 'rgb(0, 0 , 0)',
                showrivers=True,
                rivercolor='rgb(255, 255 , 255)',
                showsubunits=True
            )
        )

        return figure

    # loading dataframe to use in datatable
    cities_only_df=txt_to_dataframe()
    #selecting relevant fields only
    cities_only_df=cities_only_df[['Country Name','City Name']].copy()


    # Create Dash object
    app = dash.Dash(__name__)

    # Creating app layout
    app.layout=html.Div([
    html.Div([html.H1('Ancient Greek Colonisation')],style={'textAlign': 'center','display': 'inline-block','width':'100%'}),
    html.Div([
    dcc.Graph(id='bubble-map',figure=generate_bubble_map())
    ],style={'width': '70%', 'display': 'inline-block'}),
    html.Div([dcc.Dropdown(
    id='select-country',
    options=[{'label': k, 'value': k} for k in cities_only_df['Country Name'].unique()],
    multi=False,
    value='Turkey'),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i} for i in cities_only_df.columns
        ],
        data=cities_only_df.to_dict('records'),
        style_header={'backgroundColor': 'rgb(0, 35, 102)','fontWeight': 'bold','color':'white'},
        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(204, 204, 255)'}],
        style_cell={'textAlign': 'center'},
        style_as_list_view=True,
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable=False,
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        hidden_columns=['Country Name'])
    ],style={'width': '15%', 'display': 'inline-block','float':'right','margin-top':'50px','margin-right':'80px'})
    ])

    ###  CALLBACK TO FILTER DATATABLE
    @app.callback(Output('datatable-interactivity','data'), [Input('select-country', 'value')])
    def filter_table(selected_country):
        filtered_datatable_df=cities_only_df[cities_only_df['Country Name']== selected_country]
        return filtered_datatable_df.to_dict('records')

    return app


# Assign Dash object to variable app
app=create_app()

# import webbrowser module
import webbrowser

# Register webbrowser
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))

# Run server
if __name__ == '__main__':
        webbrowser.get('chrome').open_new('http://127.0.0.1:8050/')
        app.run_server(debug=False)
