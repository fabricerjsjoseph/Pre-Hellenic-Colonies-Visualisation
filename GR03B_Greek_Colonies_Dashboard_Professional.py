"""
Ancient Greek Colonisation Explorer - Professional Dashboard
A sophisticated, interactive visualization of Pre-Hellenic Greek settlements
"""

import dash
from dash import dcc, html, dash_table, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from GR03A_DataFrame import create_df_for_viz, txt_to_dataframe

# Professional color palette inspired by ancient Greece
THEME_COLORS = {
    'primary': '#2C3E50',      # Deep blue-gray
    'secondary': '#3498DB',    # Bright blue
    'accent': '#E74C3C',       # Terracotta red
    'success': '#27AE60',      # Olive green
    'warning': '#F39C12',      # Golden amber
    'light': '#ECF0F1',        # Light gray
    'dark': '#34495E',         # Dark blue-gray
    'ocean': '#5DADE2',        # Ocean blue
    'land': '#D5DBDB',         # Light land
}

# Colony category colors
CATEGORY_COLORS = {
    '90+ colonies': '#C0392B',        # Deep red
    '60 - 90 colonies': '#E67E22',    # Orange
    '30 - 60 colonies': '#F39C12',    # Amber
    '10 - 20 colonies': '#27AE60',    # Green
    'Less than 10 colonies': '#3498DB' # Blue
}

def create_professional_app():
    """Create the enhanced professional dashboard application"""
    
    # Load data
    df = create_df_for_viz()
    cities_df = txt_to_dataframe()
    cities_only_df = cities_df[['Country Name', 'City Name']].copy()
    
    # Calculate summary statistics
    total_colonies = df['No of Cities'].sum()
    total_countries = len(df)
    avg_colonies = df['No of Cities'].mean()
    max_country = df.loc[df['No of Cities'].idxmax(), 'Country']
    max_colonies = df['No of Cities'].max()
    
    # Create Dash app with Bootstrap theme
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.LUX, dbc.icons.FONT_AWESOME],
        suppress_callback_exceptions=True
    )
    
    def generate_map(selected_country=None, zoom_config=None):
        """Generate the interactive bubble map"""
        plot_df = df.copy()
        
        # Adjust marker size and opacity based on selection
        if selected_country and selected_country != 'ALL':
            plot_df['marker_size'] = plot_df.apply(
                lambda row: row['No of Cities'] * 30 if row['Country'] == selected_country else row['No of Cities'] * 15,
                axis=1
            )
            plot_df['marker_opacity'] = plot_df.apply(
                lambda row: 1.0 if row['Country'] == selected_country else 0.3,
                axis=1
            )
        else:
            plot_df['marker_size'] = plot_df['No of Cities'] * 22
            plot_df['marker_opacity'] = 0.85
        
        # Create scatter geo plot
        fig = px.scatter_geo(
            plot_df,
            lon='Longitude',
            lat='Latitude',
            color='Category',
            size='marker_size',
            hover_name='Country',
            hover_data={
                'No of Cities': True,
                'Longitude': False,
                'Latitude': False,
                'marker_size': False,
                'marker_opacity': False,
                'Category': True
            },
            color_discrete_map=CATEGORY_COLORS,
            size_max=55,
            custom_data=['Country', 'No of Cities']
        )
        
        # Update marker styling
        for trace in fig.data:
            trace.marker.line = dict(color='white', width=2)
            if selected_country and selected_country != 'ALL':
                category = trace.name
                cat_data = plot_df[plot_df['Category'] == category]
                trace.marker.opacity = cat_data['marker_opacity'].tolist()
            else:
                trace.marker.opacity = 0.85
        
        # Configure map zoom
        geo_config = {
            'projection_type': 'natural earth',
            'showland': True,
            'landcolor': THEME_COLORS['land'],
            'showocean': True,
            'oceancolor': THEME_COLORS['ocean'],
            'showlakes': True,
            'lakecolor': '#AED6F1',
            'showrivers': True,
            'rivercolor': '#5DADE2',
            'showcountries': True,
            'countrycolor': '#95A5A6',
            'countrywidth': 1.5,
            'showcoastlines': True,
            'coastlinecolor': THEME_COLORS['dark'],
            'coastlinewidth': 1.8,
            'showframe': True,
            'framecolor': '#BDC3C7',
            'framewidth': 2,
            'bgcolor': '#F8F9FA',
        }
        
        # Zoom to selected country
        if selected_country and selected_country != 'ALL':
            country_data = df[df['Country'] == selected_country].iloc[0]
            geo_config.update({
                'center': dict(lon=country_data['Longitude'], lat=country_data['Latitude']),
                'projection_scale': 15
            })
        else:
            geo_config.update({
                'center': dict(lon=20, lat=40),
                'projection_scale': 3.5
            })
        
        # Update layout
        fig.update_layout(
            title={
                'text': '<b style="font-family: Cinzel, Garamond, serif; font-size: 26px;">Ancient Greek Colonies Distribution</b><br>' +
                        '<sub style="color: #7F8C8D;">Pre-Hellenic Period (Before Philip II of Macedon)</sub>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': THEME_COLORS['primary']}
            },
            showlegend=True,
            height=700,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.08,
                xanchor='center',
                x=0.5,
                font=dict(size=11),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor=THEME_COLORS['secondary'],
                borderwidth=2,
                title=None
            ),
            margin=dict(l=0, r=0, t=80, b=0),
            geo=geo_config,
            paper_bgcolor='white',
            plot_bgcolor='white',
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial"
            )
        )
        
        # Customize hover template
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'Colonies: %{customdata[1]}<br>' +
                         '<extra></extra>'
        )
        
        return fig
    
    def generate_top_countries_bar():
        """Generate horizontal bar chart for top 10 countries"""
        df_sorted = df.sort_values('No of Cities', ascending=True).tail(10)
        
        fig = go.Figure(data=[
            go.Bar(
                y=df_sorted['Country'],
                x=df_sorted['No of Cities'],
                orientation='h',
                marker=dict(
                    color=THEME_COLORS['secondary'],
                    line=dict(color='white', width=2)
                ),
                text=df_sorted['No of Cities'],
                textposition='outside',
                textfont=dict(size=12, color=THEME_COLORS['primary']),
                hovertemplate='<b>%{y}</b><br>Colonies: %{x}<extra></extra>',
                customdata=df_sorted['Country']
            )
        ])
        
        fig.update_layout(
            title={
                'text': '<b>Top 10 Countries by Colony Count</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': THEME_COLORS['primary']}
            },
            xaxis_title='Number of Colonies',
            yaxis_title='',
            height=400,
            margin=dict(l=10, r=60, t=60, b=40),
            paper_bgcolor='white',
            plot_bgcolor='#F8F9FA',
            font=dict(size=12, color=THEME_COLORS['dark']),
            xaxis=dict(gridcolor='#E0E0E0', showgrid=True),
            yaxis=dict(gridcolor='#E0E0E0', showgrid=False),
            hovermode='closest'
        )
        
        return fig
    
    def generate_category_distribution_bar():
        """Generate horizontal bar chart for colony range distribution (replacing pie chart)"""
        category_counts = df.groupby('Category').size().reset_index(name='Count')
        
        # Sort by colony range (reverse order for better visualization)
        category_order = ['90+ colonies', '60 - 90 colonies', '30 - 60 colonies', '10 - 20 colonies', 'Less than 10 colonies']
        category_counts['Category'] = pd.Categorical(category_counts['Category'], categories=category_order, ordered=True)
        category_counts = category_counts.sort_values('Category', ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=category_counts['Category'],
                x=category_counts['Count'],
                orientation='h',
                marker=dict(
                    color=[CATEGORY_COLORS[cat] for cat in category_counts['Category']],
                    line=dict(color='white', width=2)
                ),
                text=category_counts['Count'],
                textposition='outside',
                textfont=dict(size=12, color=THEME_COLORS['primary']),
                hovertemplate='<b>%{y}</b><br>Countries: %{x}<br>Percentage: %{customdata:.1f}%<extra></extra>',
                customdata=[(count / len(df) * 100) for count in category_counts['Count']]
            )
        ])
        
        fig.update_layout(
            title={
                'text': '<b>Distribution by Colony Range</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': THEME_COLORS['primary']}
            },
            xaxis_title='Number of Countries',
            yaxis_title='',
            height=350,
            margin=dict(l=10, r=60, t=60, b=40),
            paper_bgcolor='white',
            plot_bgcolor='#F8F9FA',
            font=dict(size=11, color=THEME_COLORS['dark']),
            xaxis=dict(gridcolor='#E0E0E0', showgrid=True),
            yaxis=dict(gridcolor='#E0E0E0', showgrid=False)
        )
        
        return fig
    
    # Build the layout
    app.layout = dbc.Container([
        # Header with elegant styling
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(
                        '🏛️ Ancient Greek Colonisation Explorer',
                        className='text-center mb-2',
                        style={
                            'fontFamily': 'Cinzel, Garamond, serif',
                            'fontWeight': 'bold',
                            'color': THEME_COLORS['primary'],
                            'textShadow': '2px 2px 4px rgba(0,0,0,0.1)',
                            'fontSize': '3rem'
                        }
                    ),
                    html.P(
                        'Interactive Visualization of Pre-Hellenic Greek Settlements Across the Mediterranean',
                        className='text-center text-muted',
                        style={'fontSize': '1.1rem', 'fontStyle': 'italic'}
                    ),
                ], style={
                    'padding': '30px',
                    'background': f'linear-gradient(135deg, {THEME_COLORS["light"]} 0%, white 100%)',
                    'borderBottom': f'4px solid {THEME_COLORS["secondary"]}',
                    'borderRadius': '0 0 15px 15px'
                })
            ], width=12)
        ], className='mb-4'),
        
        # KPI Cards Row with Icons
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className='fas fa-city fa-2x mb-2', style={'color': THEME_COLORS['secondary']}),
                            html.H3(id='total-colonies-value', children=str(total_colonies), className='mb-0', style={'color': THEME_COLORS['primary'], 'fontWeight': 'bold'}),
                            html.P('Total Colonies', className='text-muted mb-0', style={'fontSize': '0.9rem'})
                        ], className='text-center')
                    ])
                ], className='shadow-sm h-100', style={'borderTop': f'3px solid {THEME_COLORS["secondary"]}'})
            ], width=12, lg=3, className='mb-3'),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className='fas fa-flag fa-2x mb-2', style={'color': THEME_COLORS['success']}),
                            html.H3(id='total-countries-value', children=str(total_countries), className='mb-0', style={'color': THEME_COLORS['primary'], 'fontWeight': 'bold'}),
                            html.P('Countries', className='text-muted mb-0', style={'fontSize': '0.9rem'})
                        ], className='text-center')
                    ])
                ], className='shadow-sm h-100', style={'borderTop': f'3px solid {THEME_COLORS["success"]}'})
            ], width=12, lg=3, className='mb-3'),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className='fas fa-chart-line fa-2x mb-2', style={'color': THEME_COLORS['warning']}),
                            html.H3(id='avg-colonies-value', children=f'{avg_colonies:.1f}', className='mb-0', style={'color': THEME_COLORS['primary'], 'fontWeight': 'bold'}),
                            html.P('Avg per Country', className='text-muted mb-0', style={'fontSize': '0.9rem'})
                        ], className='text-center')
                    ])
                ], className='shadow-sm h-100', style={'borderTop': f'3px solid {THEME_COLORS["warning"]}'})
            ], width=12, lg=3, className='mb-3'),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className='fas fa-crown fa-2x mb-2', style={'color': THEME_COLORS['accent']}),
                            html.H3(id='top-country-name', children=max_country, className='mb-0', style={'color': THEME_COLORS['primary'], 'fontWeight': 'bold', 'fontSize': '1.5rem'}),
                            html.P(id='top-country-count', children=f'{max_colonies} colonies', className='text-muted mb-0', style={'fontSize': '0.9rem'})
                        ], className='text-center')
                    ])
                ], className='shadow-sm h-100', style={'borderTop': f'3px solid {THEME_COLORS["accent"]}'})
            ], width=12, lg=3, className='mb-3'),
        ], className='mb-4'),
        
        # Main Content: Two-Column Layout
        dbc.Row([
            # Left Column: Map (Main Focus)
            dbc.Col([
                # Control Panel
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    html.I(className='fas fa-search me-2'),
                                    'Select Country:'
                                ], style={'fontWeight': 'bold', 'fontSize': '1rem'}),
                                dcc.Dropdown(
                                    id='country-selector',
                                    options=[{'label': '🌍 All Countries', 'value': 'ALL'}] + 
                                            [{'label': k, 'value': k} for k in sorted(df['Country'].unique())],
                                    value='ALL',
                                    clearable=False,
                                    className='mb-2'
                                ),
                            ], width=8),
                            dbc.Col([
                                html.Label('\u00A0', style={'display': 'block'}),  # Spacer
                                dbc.Button(
                                    [html.I(className='fas fa-redo me-2'), 'Reset View'],
                                    id='reset-button',
                                    color='primary',
                                    className='w-100',
                                    n_clicks=0
                                ),
                            ], width=4),
                        ]),
                        html.Hr(),
                        html.Div(id='selected-info', className='mt-2')
                    ])
                ], className='shadow-sm mb-3'),
                
                # Map
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='bubble-map',
                            figure=generate_map(),
                            config={'displayModeBar': True, 'scrollZoom': True}
                        )
                    ], className='p-2')
                ], className='shadow')
            ], width=12, lg=7, className='mb-4'),
            
            # Right Column: Charts and Table (Details Panel)
            dbc.Col([
                # Top Countries Bar Chart
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='bar-chart',
                            figure=generate_top_countries_bar(),
                            config={'displayModeBar': False}
                        )
                    ], className='p-2')
                ], className='shadow-sm mb-3'),
                
                # Category Distribution Bar Chart (replacing pie)
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(
                            id='category-chart',
                            figure=generate_category_distribution_bar(),
                            config={'displayModeBar': False}
                        )
                    ], className='p-2')
                ], className='shadow-sm mb-3'),
                
                # Colony Details Table
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className='fas fa-table me-2'),
                            'Colony Details'
                        ], className='text-center mb-3', style={'color': THEME_COLORS['primary']}),
                        dash_table.DataTable(
                            id='datatable-interactivity',
                            columns=[
                                {"name": "Country", "id": "Country Name"},
                                {"name": "City Name", "id": "City Name"}
                            ],
                            data=cities_only_df.to_dict('records'),
                            style_header={
                                'backgroundColor': THEME_COLORS['primary'],
                                'fontWeight': 'bold',
                                'color': 'white',
                                'textAlign': 'center',
                                'fontSize': '13px',
                                'padding': '12px',
                                'border': '1px solid #ddd'
                            },
                            style_data={
                                'backgroundColor': 'white',
                                'color': THEME_COLORS['dark'],
                                'fontSize': '12px',
                                'textAlign': 'center',
                                'border': '1px solid #ddd'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': THEME_COLORS['light']
                                },
                                {
                                    'if': {'state': 'selected'},
                                    'backgroundColor': '#D6EAF8',
                                    'border': f'2px solid {THEME_COLORS["secondary"]}'
                                }
                            ],
                            style_cell={
                                'textAlign': 'center',
                                'padding': '10px',
                                'minWidth': '80px',
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            },
                            style_table={
                                'overflowX': 'auto'
                            },
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",
                            page_action="native",
                            page_current=0,
                            page_size=12,
                            row_selectable=False
                        )
                    ])
                ], className='shadow-sm')
            ], width=12, lg=5, className='mb-4'),
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P([
                        html.I(className='fas fa-database me-2'),
                        'Data Source: ',
                        html.A('Wikipedia - Greek Colonisation',
                               href='https://en.wikipedia.org/wiki/Greek_colonisation',
                               target='_blank',
                               style={'color': THEME_COLORS['secondary'], 'textDecoration': 'none'})
                    ], className='text-center mb-0', style={'color': 'white', 'fontSize': '0.9rem'})
                ], style={
                    'padding': '20px',
                    'backgroundColor': THEME_COLORS['primary'],
                    'borderRadius': '10px 10px 0 0'
                })
            ], width=12)
        ], className='mt-4')
    ], fluid=True, style={'backgroundColor': '#F8F9FA', 'minHeight': '100vh', 'padding': '0'})
    
    # Comprehensive Cross-Filtering Callbacks
    @app.callback(
        [
            Output('bubble-map', 'figure'),
            Output('datatable-interactivity', 'data'),
            Output('datatable-interactivity', 'columns'),
            Output('selected-info', 'children'),
            Output('total-colonies-value', 'children'),
            Output('total-countries-value', 'children'),
            Output('avg-colonies-value', 'children'),
            Output('top-country-name', 'children'),
            Output('top-country-count', 'children'),
            Output('country-selector', 'value'),
        ],
        [
            Input('country-selector', 'value'),
            Input('reset-button', 'n_clicks'),
            Input('bubble-map', 'clickData'),
            Input('bar-chart', 'clickData'),
        ],
        [State('country-selector', 'value')]
    )
    def update_all_components(dropdown_value, reset_clicks, map_click, bar_click, current_dropdown):
        """Master callback for comprehensive cross-filtering"""
        
        # Determine which input triggered the callback
        triggered_id = ctx.triggered_id if ctx.triggered_id else 'country-selector'
        
        selected_country = None
        
        # Handle different triggers
        if triggered_id == 'reset-button':
            selected_country = 'ALL'
        elif triggered_id == 'bubble-map' and map_click:
            # Map click - extract country from click data
            selected_country = map_click['points'][0]['customdata'][0]
        elif triggered_id == 'bar-chart' and bar_click:
            # Bar chart click - extract country
            selected_country = bar_click['points'][0]['customdata']
        elif triggered_id == 'country-selector':
            selected_country = dropdown_value
        else:
            selected_country = current_dropdown if current_dropdown else 'ALL'
        
        # Ensure we have a valid selection
        if not selected_country or selected_country == 'ALL':
            selected_country = 'ALL'
        
        # Update map
        map_figure = generate_map(selected_country)
        
        # Filter data for table and stats
        if selected_country == 'ALL':
            filtered_cities = cities_only_df.copy()
            filtered_df = df.copy()
            show_country_column = True
        else:
            filtered_cities = cities_only_df[cities_only_df['Country Name'] == selected_country].copy()
            filtered_df = df[df['Country'] == selected_country].copy()
            show_country_column = False
        
        # Update table columns based on selection
        if show_country_column:
            table_columns = [
                {"name": "Country", "id": "Country Name"},
                {"name": "City Name", "id": "City Name"}
            ]
        else:
            table_columns = [{"name": "City Name", "id": "City Name"}]
        
        # Calculate updated statistics
        if selected_country == 'ALL':
            stats_colonies = total_colonies
            stats_countries = total_countries
            stats_avg = avg_colonies
            stats_top_name = max_country
            stats_top_count = max_colonies
        else:
            country_data = df[df['Country'] == selected_country].iloc[0]
            stats_colonies = country_data['No of Cities']
            stats_countries = 1
            stats_avg = country_data['No of Cities']
            stats_top_name = selected_country
            stats_top_count = country_data['No of Cities']
        
        # Update info panel
        if selected_country == 'ALL':
            info_content = dbc.Alert([
                html.H5([html.I(className='fas fa-info-circle me-2'), 'Overview'], className='mb-2'),
                html.P([html.Strong('Total Colonies: '), f'{total_colonies}'], className='mb-1'),
                html.P([html.Strong('Countries: '), f'{total_countries}'], className='mb-1'),
                html.P('Select a country from the dropdown, click on the map, or click a bar in the chart to explore details.', className='mb-0 small fst-italic')
            ], color='info', className='mb-0')
        else:
            country_data = df[df['Country'] == selected_country].iloc[0]
            info_content = dbc.Alert([
                html.H5([html.I(className='fas fa-map-marker-alt me-2'), selected_country], className='mb-2'),
                html.P([html.Strong('Colonies: '), f'{country_data["No of Cities"]}'], className='mb-1'),
                html.P([html.Strong('Category: '), country_data['Category']], className='mb-1'),
                html.P([html.Strong('Cities Displayed: '), f'{len(filtered_cities)}'], className='mb-0'),
            ], color='success', className='mb-0')
        
        return (
            map_figure,
            filtered_cities.to_dict('records'),
            table_columns,
            info_content,
            str(stats_colonies),
            str(stats_countries),
            f'{stats_avg:.1f}',
            stats_top_name,
            f'{stats_top_count} colonies',
            selected_country
        )
    
    return app


if __name__ == '__main__':
    app = create_professional_app()
    print("=" * 70)
    print("🏛️  ANCIENT GREEK COLONISATION EXPLORER - PROFESSIONAL EDITION")
    print("=" * 70)
    print("\n✨ Enhanced Features:")
    print("   • Modern Bootstrap LUX theme with elegant design")
    print("   • Two-column responsive layout (Map + Details)")
    print("   • FontAwesome icons on KPI cards")
    print("   • Automatic map zoom on country selection")
    print("   • Horizontal bar chart replacing pie chart")
    print("   • Comprehensive cross-filtering:")
    print("     - Dropdown → All components")
    print("     - Map click → All components")
    print("     - Bar chart click → All components")
    print("   • Reset button restores global view")
    print("   • Dynamic KPI updates based on selection")
    print("\n🌐 Open your browser at: http://127.0.0.1:8050/")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 70)
    app.run(debug=False, port=8050)
