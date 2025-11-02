import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from GR03A_DataFrame import create_df_for_viz, txt_to_dataframe

# Color palette constants
COLORS = {
    '90+ colonies': '#FF6B6B',          # Coral red
    '60 - 90 colonies': '#4ECDC4',      # Turquoise
    '30 - 60 colonies': '#FFE66D',      # Golden yellow
    '10 - 20 colonies': '#95E1D3',      # Mint green
    'Less than 10 colonies': '#A8E6CF'  # Light mint
}

# UI constants
STATS_CARD_WIDTH = '20%'
TOP_COUNTRY_CARD_WIDTH = '38%'
MAP_COLUMN_WIDTH = '65%'
CHARTS_COLUMN_WIDTH = '33%'

def create_enhanced_app():
    # Load dataframes
    df = create_df_for_viz()
    cities_df = txt_to_dataframe()
    cities_only_df = cities_df[['Country Name', 'City Name']].copy()
    
    # Create enhanced bubble map
    def generate_enhanced_bubble_map(selected_country=None):
        fig = go.Figure()
        
        # Add traces for each category
        for category in df['Category'].unique():
            df_cat = df[df.Category == category]
            
            # Highlight selected country
            if selected_country:
                sizes = []
                opacities = []
                for country in df_cat['Country']:
                    if country == selected_country:
                        sizes.append(df_cat[df_cat['Country'] == country]['No of Cities'].values[0] * 25)
                        opacities.append(1.0)
                    else:
                        sizes.append(df_cat[df_cat['Country'] == country]['No of Cities'].values[0] * 20)
                        opacities.append(0.4)
            else:
                sizes = df_cat['No of Cities'] * 22
                opacities = [0.8] * len(df_cat)
            
            fig.add_trace(go.Scattergeo(
                lon=df_cat.Longitude,
                lat=df_cat.Latitude,
                text=df_cat.Trace_Text,
                mode='markers',
                marker=dict(
                    size=sizes if selected_country else df_cat['No of Cities'] * 22,
                    color=COLORS[category],
                    line=dict(
                        color='white',
                        width=2
                    ),
                    sizemode='area',
                    opacity=opacities if selected_country else 0.8
                ),
                name=category,
                customdata=df_cat[['Country', 'No of Cities']],
                hovertemplate='<b>%{customdata[0]}</b><br>' +
                              'Colonies: %{customdata[1]}<br>' +
                              '<extra></extra>'
            ))
        
        # Enhanced layout with better styling
        fig.update_layout(
            title={
                'text': '<b>Ancient Greek Colonies Distribution</b><br>' +
                        '<sub>Pre-Hellenic Period (Before Philip II of Macedon)</sub>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2C3E50', 'family': 'Arial Black'}
            },
            showlegend=True,
            width=1200,
            height=800,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.15,
                xanchor='center',
                x=0.5,
                font=dict(size=12),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#E0E0E0',
                borderwidth=2
            ),
            margin=dict(l=0, r=0, t=80, b=100),
            geo=dict(
                center=dict(lon=20.2, lat=41.2),
                projection=dict(scale=7),
                showcoastlines=True,
                coastlinecolor='#95A5A6',
                coastlinewidth=1.5,
                showcountries=True,
                countrycolor='#BDC3C7',
                countrywidth=1,
                showframe=False,
                landcolor='#34495E',
                showlakes=True,
                lakecolor='#2980B9',
                showrivers=True,
                rivercolor='#3498DB',
                showsubunits=True,
                bgcolor='#1A252F'
            ),
            paper_bgcolor='#ECF0F1',
            plot_bgcolor='#ECF0F1'
        )
        
        return fig
    
    # Create bar chart for top countries
    def generate_bar_chart():
        df_sorted = df.sort_values('No of Cities', ascending=True).tail(10)
        
        fig = go.Figure(data=[
            go.Bar(
                y=df_sorted['Country'],
                x=df_sorted['No of Cities'],
                orientation='h',
                marker=dict(
                    color=df_sorted['No of Cities'],
                    colorscale='Viridis',
                    showscale=False,
                    line=dict(color='white', width=1)
                ),
                text=df_sorted['No of Cities'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Colonies: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '<b>Top 10 Countries by Colony Count</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#2C3E50'}
            },
            xaxis_title='Number of Colonies',
            yaxis_title='',
            height=400,
            margin=dict(l=10, r=10, t=50, b=40),
            paper_bgcolor='white',
            plot_bgcolor='#F8F9FA',
            font=dict(size=11),
            xaxis=dict(gridcolor='#E0E0E0'),
            yaxis=dict(gridcolor='#E0E0E0')
        )
        
        return fig
    
    # Create pie chart for category distribution
    def generate_pie_chart():
        category_counts = df.groupby('Category').size().reset_index(name='Count')
        
        fig = go.Figure(data=[
            go.Pie(
                labels=category_counts['Category'],
                values=category_counts['Count'],
                marker=dict(
                    colors=[COLORS[cat] for cat in category_counts['Category']],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(size=12),
                hovertemplate='<b>%{label}</b><br>Countries: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '<b>Distribution by Colony Range</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#2C3E50'}
            },
            height=400,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='white',
            showlegend=True,
            legend=dict(font=dict(size=10))
        )
        
        return fig
    
    # Calculate summary statistics
    total_colonies = df['No of Cities'].sum()
    total_countries = len(df)
    avg_colonies = df['No of Cities'].mean()
    max_country = df.loc[df['No of Cities'].idxmax(), 'Country']
    max_colonies = df['No of Cities'].max()
    
    # Create Dash app
    app = dash.Dash(__name__)
    
    # Enhanced layout with modern design
    app.layout = html.Div([
        # Header Section
        html.Div([
            html.H1(
                '🏛️ Ancient Greek Colonisation Explorer',
                style={
                    'textAlign': 'center',
                    'color': '#2C3E50',
                    'marginBottom': '10px',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '42px',
                    'fontWeight': 'bold',
                    'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
                }
            ),
            html.P(
                'Interactive visualization of Pre-Hellenic Greek settlements across the Mediterranean',
                style={
                    'textAlign': 'center',
                    'color': '#7F8C8D',
                    'fontSize': '16px',
                    'marginBottom': '20px',
                    'fontFamily': 'Arial, sans-serif'
                }
            )
        ], style={
            'backgroundColor': '#ECF0F1',
            'padding': '20px',
            'borderBottom': '3px solid #3498DB'
        }),
        
        # Statistics Cards Row
        html.Div([
            # Card 1: Total Colonies
            html.Div([
                html.Div([
                    html.H3('Total Colonies', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(str(total_colonies), style={'color': '#2C3E50', 'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0'}),
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'textAlign': 'center'
                })
            ], style={'width': '20%', 'display': 'inline-block', 'padding': '10px'}),
            
            # Card 2: Countries
            html.Div([
                html.Div([
                    html.H3('Countries', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(str(total_countries), style={'color': '#2C3E50', 'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0'}),
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'textAlign': 'center'
                })
            ], style={'width': STATS_CARD_WIDTH, 'display': 'inline-block', 'padding': '10px'}),
            
            # Card 3: Average
            html.Div([
                html.Div([
                    html.H3('Avg per Country', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(f'{avg_colonies:.1f}', style={'color': '#2C3E50', 'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0'}),
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'textAlign': 'center'
                })
            ], style={'width': STATS_CARD_WIDTH, 'display': 'inline-block', 'padding': '10px'}),
            
            # Card 4: Top Country
            html.Div([
                html.Div([
                    html.H3('Most Colonies', style={'color': '#7F8C8D', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(max_country, style={'color': '#2C3E50', 'fontSize': '24px', 'fontWeight': 'bold', 'margin': '0'}),
                    html.P(f'{max_colonies} colonies', style={'color': '#7F8C8D', 'fontSize': '12px', 'margin': '5px 0 0 0'}),
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'textAlign': 'center'
                })
            ], style={'width': TOP_COUNTRY_CARD_WIDTH, 'display': 'inline-block', 'padding': '10px'}),
        ], style={
            'backgroundColor': '#ECF0F1',
            'padding': '10px 20px',
            'textAlign': 'center'
        }),
        
        # Main Content Row
        html.Div([
            # Left Column - Map and Controls
            html.Div([
                # Control Panel
                html.Div([
                    html.Label('🔍 Select Country:', style={
                        'fontWeight': 'bold',
                        'color': '#2C3E50',
                        'marginBottom': '10px',
                        'fontSize': '14px'
                    }),
                    dcc.Dropdown(
                        id='country-selector',
                        options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                                [{'label': k, 'value': k} for k in sorted(df['Country'].unique())],
                        value='ALL',
                        style={
                            'marginBottom': '15px',
                            'fontSize': '14px'
                        },
                        clearable=False
                    ),
                    html.Button(
                        '🔄 Reset View',
                        id='reset-button',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'padding': '10px',
                            'backgroundColor': '#3498DB',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '5px',
                            'cursor': 'pointer',
                            'fontSize': '14px',
                            'fontWeight': 'bold',
                            'marginBottom': '10px'
                        }
                    ),
                    html.Div(id='selected-info', style={
                        'padding': '15px',
                        'backgroundColor': '#E8F6F3',
                        'borderRadius': '5px',
                        'marginTop': '10px',
                        'fontSize': '13px',
                        'color': '#2C3E50'
                    })
                ], style={
                    'backgroundColor': 'white',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'marginBottom': '20px'
                }),
                
                # Map
                dcc.Graph(
                    id='bubble-map',
                    figure=generate_enhanced_bubble_map(),
                    style={'borderRadius': '10px', 'overflow': 'hidden'}
                )
            ], style={'width': MAP_COLUMN_WIDTH, 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
            
            # Right Column - Charts and Table
            html.Div([
                # Bar Chart
                html.Div([
                    dcc.Graph(
                        id='bar-chart',
                        figure=generate_bar_chart(),
                        style={'height': '400px'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'marginBottom': '20px',
                    'padding': '10px'
                }),
                
                # Pie Chart
                html.Div([
                    dcc.Graph(
                        id='pie-chart',
                        figure=generate_pie_chart(),
                        style={'height': '400px'}
                    )
                ], style={
                    'backgroundColor': 'white',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'marginBottom': '20px',
                    'padding': '10px'
                }),
                
                # Data Table
                html.Div([
                    html.H3('Colony Details', style={
                        'textAlign': 'center',
                        'color': '#2C3E50',
                        'fontSize': '18px',
                        'marginBottom': '15px',
                        'fontWeight': 'bold'
                    }),
                    html.Div([
                        html.Label('Search colonies:', style={
                            'fontWeight': 'bold',
                            'color': '#2C3E50',
                            'fontSize': '12px',
                            'marginBottom': '5px'
                        }),
                        dcc.Input(
                            id='search-box',
                            type='text',
                            placeholder='Type to search...',
                            style={
                                'width': '100%',
                                'padding': '8px',
                                'marginBottom': '10px',
                                'border': '1px solid #BDC3C7',
                                'borderRadius': '5px',
                                'fontSize': '12px'
                            }
                        )
                    ]),
                    dash_table.DataTable(
                        id='datatable-interactivity',
                        columns=[{"name": "City Name", "id": "City Name"}],
                        data=cities_only_df.to_dict('records'),
                        style_header={
                            'backgroundColor': '#2C3E50',
                            'fontWeight': 'bold',
                            'color': 'white',
                            'textAlign': 'center',
                            'fontSize': '12px',
                            'padding': '10px'
                        },
                        style_data={
                            'backgroundColor': 'white',
                            'color': '#2C3E50',
                            'fontSize': '11px',
                            'textAlign': 'center'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#F8F9FA'
                            },
                            {
                                'if': {'state': 'selected'},
                                'backgroundColor': '#D5DBDB',
                                'border': '1px solid #3498DB'
                            }
                        ],
                        style_cell={
                            'textAlign': 'center',
                            'padding': '8px',
                            'minWidth': '100px'
                        },
                        style_as_list_view=True,
                        editable=False,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        page_current=0,
                        page_size=15
                    )
                ], style={
                    'backgroundColor': 'white',
                    'borderRadius': '10px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
                    'padding': '20px'
                })
            ], style={'width': CHARTS_COLUMN_WIDTH, 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
        ], style={'backgroundColor': '#ECF0F1'}),
        
        # Footer
        html.Div([
            html.P([
                'Data source: ',
                html.A('Wikipedia - Greek Colonisation', 
                       href='https://en.wikipedia.org/wiki/Greek_colonisation',
                       target='_blank',
                       style={'color': '#3498DB', 'textDecoration': 'none'})
            ], style={'textAlign': 'center', 'color': '#7F8C8D', 'fontSize': '12px', 'margin': '0'})
        ], style={
            'backgroundColor': '#2C3E50',
            'padding': '15px',
            'marginTop': '20px'
        })
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#ECF0F1',
        'minHeight': '100vh'
    })
    
    # Callback for country selection and map update
    @app.callback(
        [Output('bubble-map', 'figure'),
         Output('datatable-interactivity', 'data'),
         Output('selected-info', 'children')],
        [Input('country-selector', 'value'),
         Input('reset-button', 'n_clicks'),
         Input('search-box', 'value')]
    )
    def update_visualization(selected_country, reset_clicks, search_term):
        # Handle reset button
        if selected_country == 'ALL':
            selected_country = None
        
        # Update map
        fig = generate_enhanced_bubble_map(selected_country)
        
        # Filter table data
        filtered_df = cities_only_df.copy()
        if selected_country:
            filtered_df = filtered_df[filtered_df['Country Name'] == selected_country]
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['City Name'].str.contains(search_term, case=False, na=False)
            ]
        
        # Update info panel
        if selected_country:
            country_data = df[df['Country'] == selected_country].iloc[0]
            info_text = [
                html.H4(f'📍 {selected_country}', style={'margin': '0 0 10px 0', 'color': '#2C3E50'}),
                html.P(f'Colonies: {country_data["No of Cities"]}', style={'margin': '5px 0'}),
                html.P(f'Category: {country_data["Category"]}', style={'margin': '5px 0'}),
                html.P(f'Cities displayed: {len(filtered_df)}', style={'margin': '5px 0', 'fontWeight': 'bold'})
            ]
        else:
            info_text = [
                html.H4('ℹ️ Overview', style={'margin': '0 0 10px 0', 'color': '#2C3E50'}),
                html.P(f'Total colonies: {total_colonies}', style={'margin': '5px 0'}),
                html.P(f'Countries: {total_countries}', style={'margin': '5px 0'}),
                html.P('Select a country to explore details', style={'margin': '5px 0', 'fontStyle': 'italic'})
            ]
        
        return fig, filtered_df.to_dict('records'), info_text
    
    return app

# Create and run the app
if __name__ == '__main__':
    app = create_enhanced_app()
    print("🚀 Starting Enhanced Ancient Greek Colonies Dashboard...")
    print("📊 Open your browser at: http://127.0.0.1:8050/")
    print("✨ Enhanced features:")
    print("   - Interactive country selection with highlighting")
    print("   - Summary statistics cards")
    print("   - Top countries bar chart")
    print("   - Category distribution pie chart")
    print("   - Advanced search and filtering")
    print("   - Modern, responsive design")
    print("\nPress Ctrl+C to stop the server")
    app.run(debug=False, port=8050)
