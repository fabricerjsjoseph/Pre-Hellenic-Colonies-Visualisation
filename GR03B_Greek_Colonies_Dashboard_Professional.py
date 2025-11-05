"""Ancient Greek Colonisation Explorer - Professional Dashboard
===========================================================================

This module defines a highly-polished Dash application for exploring data on
pre-Hellenic Greek settlements.  The refreshed experience focuses on three
pillars:

* A refined, responsive layout that embraces modern dashboard design
* Premium Plotly visualisations that balance aesthetics with clarity
* Advanced cross-filtering so every interaction yields actionable insight

The dashboard is intentionally expressive and cinematic, aiming to evoke the
maritime journeys of the ancient colonists whilst remaining a rigorous
analytical tool.
"""

from __future__ import annotations

import math
from typing import Optional, Sequence, Tuple

import dash
from dash import Input, Output, State, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from GR03A_DataFrame import create_df_for_viz, txt_to_dataframe


# ---------------------------------------------------------------------------
# Styling constants inspired by Aegean palettes and classical architecture
# ---------------------------------------------------------------------------

THEME_COLORS = {
    "primary": "#1E2A38",  # Midnight blue
    "secondary": "#2A8CCB",  # Aegean teal
    "accent": "#E67E22",  # Burnt ochre
    "success": "#27AE60",  # Laurel green
    "warning": "#F1C40F",  # Sunlit gold
    "light": "#F6F7F9",  # Porcelain white
    "dark": "#111C26",  # Deep navy
    "ocean": "#5DADE2",  # Crystal blue
    "sand": "#E8D3A5",  # Coastal sand
}

CATEGORY_COLORS = {
    "90+ colonies": "#C0392B",
    "60 - 90 colonies": "#E67E22",
    "30 - 60 colonies": "#F1C40F",
    "10 - 20 colonies": "#27AE60",
    "Less than 10 colonies": "#2980B9",
}

PROJECTION_OPTIONS = [
    {"label": "Natural Earth", "value": "natural earth"},
    {"label": "Orthographic", "value": "orthographic"},
    {"label": "Mercator", "value": "mercator"},
]


def create_professional_app() -> dash.Dash:
    """Create the enhanced professional dashboard application."""

    # ------------------------------------------------------------------
    # Load and prepare data
    # ------------------------------------------------------------------
    df = create_df_for_viz()
    cities_df = txt_to_dataframe()
    cities_df = cities_df.rename(columns={"Country Name": "Country", "City Name": "City"})

    # Derive summary statistics
    total_colonies = int(df["No of Cities"].sum())
    total_countries = int(df["Country"].nunique())
    avg_colonies = float(df["No of Cities"].mean())
    max_country_row = df.loc[df["No of Cities"].idxmax()]
    max_country = str(max_country_row["Country"])
    max_colonies = int(max_country_row["No of Cities"])

    # Range for slider controls
    min_colonies = int(math.floor(df["No of Cities"].min()))
    max_colonies_range = int(math.ceil(df["No of Cities"].max()))

    # Dash application
    app = dash.Dash(
        __name__,
        title="Ancient Greek Colonisation Explorer",
        external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME],
        suppress_callback_exceptions=True,
    )

    app.index_string = """
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                body {background: radial-gradient(circle at top, #0B1C2C, #02050A);} 
                .dbc {font-family: 'Montserrat', 'Segoe UI', sans-serif;}
                .hero-gradient {background: linear-gradient(135deg, rgba(46,134,193,0.95), rgba(17,28,38,0.85));}
            </style>
        </head>
        <body class="dbc">
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    """

    # ------------------------------------------------------------------
    # Helper builders
    # ------------------------------------------------------------------

    def build_hero_banner() -> dbc.Row:
        return dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("Ancient Greek Colonisation", className="text-uppercase fw-bold small"),
                                html.H1(
                                    "Mediterranean Expedition Dashboard",
                                    className="display-5 fw-bold text-white mt-1",
                                ),
                                html.P(
                                    "Navigate the maritime spread of Hellenic influence before the rise of Philip II of Macedon.",
                                    className="lead text-white-50 mb-3",
                                ),
                                dbc.Badge(
                                    f"{total_colonies} catalogued colonies across {total_countries} host regions",
                                    color="info",
                                    pill=True,
                                    className="px-3 py-2",
                                ),
                            ],
                            className="hero-gradient text-white p-4 rounded-4 shadow",
                        ),
                    ],
                    className="p-1",
                ),
                width=12,
            ),
            className="mb-4 mt-3",
        )

    def build_metric_cards() -> dbc.Row:
        cards = [
            ("fas fa-city", "Total Colonies", str(total_colonies), THEME_COLORS["secondary"]),
            ("fas fa-flag", "Countries", str(total_countries), THEME_COLORS["success"]),
            ("fas fa-chart-line", "Average per Country", f"{avg_colonies:.1f}", THEME_COLORS["warning"]),
            ("fas fa-crown", "Most Prolific", max_country, THEME_COLORS["accent"]),
        ]

        columns = []
        for icon, title, value, color in cards:
            columns.append(
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        html.I(className=f"{icon} fa-lg mb-3", style={"color": color}),
                                        html.H4(value, className="fw-bold text-white"),
                                        html.Div(title, className="text-uppercase text-muted small"),
                                    ],
                                    className="text-center",
                                )
                            ],
                            className="py-3",
                        ),
                        className="glass-card h-100 border-0",
                        style={"background": "rgba(255,255,255,0.06)", "backdropFilter": "blur(6px)"},
                    ),
                    xs=12,
                    sm=6,
                    lg=3,
                    className="mb-3",
                )
            )
        return dbc.Row(columns, className="mb-4")

    def build_control_panel() -> dbc.Card:
        category_options = [
            {"label": html.Span(cat, className="ms-1"), "value": cat} for cat in CATEGORY_COLORS.keys()
        ]

        return dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        [html.I(className="fas fa-compass me-2"), "Focus Country"],
                                        className="fw-bold text-light",
                                    ),
                                    dcc.Dropdown(
                                        id="country-selector",
                                        options=[{"label": "🌍 All Countries", "value": "ALL"}]
                                        + [
                                            {"label": country, "value": country}
                                            for country in sorted(df["Country"].unique())
                                        ],
                                        value="ALL",
                                        clearable=False,
                                        className="text-dark",
                                    ),
                                    html.Div(id="filter-summary", className="small text-white-50 mt-2"),
                                ],
                                lg=4,
                                className="mb-3",
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        [html.I(className="fas fa-layer-group me-2"), "Colony Intensity"],
                                        className="fw-bold text-light",
                                    ),
                                    dcc.RangeSlider(
                                        id="colony-range-slider",
                                        min=min_colonies,
                                        max=max_colonies_range,
                                        step=1,
                                        value=[min_colonies, max_colonies_range],
                                        marks={
                                            min_colonies: str(min_colonies),
                                            max_colonies_range: str(max_colonies_range),
                                        },
                                        tooltip={"placement": "bottom", "always_visible": False},
                                    ),
                                ],
                                lg=4,
                                className="mb-3",
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        [html.I(className="fas fa-palette me-2"), "Colony Bands"],
                                        className="fw-bold text-light",
                                    ),
                                    dbc.Checklist(
                                        id="category-checklist",
                                        options=category_options,
                                        value=list(CATEGORY_COLORS.keys()),
                                        inline=True,
                                        switch=True,
                                        className="text-white-50",
                                    ),
                                ],
                                lg=4,
                                className="mb-3",
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        [html.I(className="fas fa-globe me-2"), "Map Projection"],
                                        className="fw-bold text-light",
                                    ),
                                    dbc.RadioItems(
                                        id="projection-selector",
                                        options=PROJECTION_OPTIONS,
                                        value="natural earth",
                                        inline=True,
                                        className="text-white-50",
                                    ),
                                ],
                                lg=6,
                                className="mb-2",
                            ),
                            dbc.Col(
                                [
                                    html.Label(
                                        [html.I(className="fas fa-adjust me-2"), "Marker Emphasis"],
                                        className="fw-bold text-light",
                                    ),
                                    dbc.RadioItems(
                                        id="marker-mode",
                                        options=[
                                            {"label": "Scale by colonies", "value": "scaled"},
                                            {"label": "Uniform", "value": "uniform"},
                                        ],
                                        value="scaled",
                                        inline=True,
                                        className="text-white-50",
                                    ),
                                ],
                                lg=6,
                                className="mb-2",
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    [html.I(className="fas fa-sync-alt me-2"), "Reset Filters"],
                                    id="reset-button",
                                    color="primary",
                                    outline=True,
                                    className="me-2",
                                ),
                                lg=3,
                                className="d-grid mb-2",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    [html.I(className="fas fa-file-download me-2"), "Download Snapshot"],
                                    id="download-button",
                                    color="info",
                                    outline=True,
                                ),
                                lg=3,
                                className="d-grid mb-2",
                            ),
                            dbc.Col(
                                html.Div(id="insight-panel"),
                                lg=6,
                            ),
                        ],
                        className="align-items-center mt-2",
                    ),
                ]
            ),
            className="border-0 shadow-sm mb-4",
            style={"background": "rgba(14,31,47,0.85)", "backdropFilter": "blur(4px)"},
        )

    def build_tabs() -> dbc.Tabs:
        return dbc.Tabs(
            [
                dbc.Tab(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(
                                            id="bubble-map",
                                            config={"displayModeBar": True, "scrollZoom": True},
                                            figure=go.Figure(),
                                            className="shadow-sm",
                                        ),
                                    ),
                                    className="border-0",
                                    style={"background": "rgba(255,255,255,0.02)"},
                                ),
                                lg=8,
                                className="mb-4",
                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            dcc.Graph(
                                                id="gauge-chart",
                                                config={"displayModeBar": False},
                                                figure=go.Figure(),
                                            )
                                        ),
                                        className="border-0 mb-3",
                                        style={"background": "rgba(255,255,255,0.02)"},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(html.Div(id="selected-info")),
                                        className="border-0",
                                        style={"background": "rgba(255,255,255,0.02)"},
                                    ),
                                ],
                                lg=4,
                                className="mb-4",
                            ),
                        ]
                    ),
                    label="Geographic Overview",
                    tab_id="tab-map",
                    tabClassName="text-light fw-semibold",
                    label_style={"padding": "12px 20px"},
                ),
                dbc.Tab(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id="bar-chart", config={"displayModeBar": False})
                                    ),
                                    className="border-0 mb-4",
                                    style={"background": "rgba(255,255,255,0.02)"},
                                ),
                                lg=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id="category-chart", config={"displayModeBar": False})
                                    ),
                                    className="border-0 mb-4",
                                    style={"background": "rgba(255,255,255,0.02)"},
                                ),
                                lg=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id="treemap-chart", config={"displayModeBar": False})
                                    ),
                                    className="border-0 mb-4",
                                    style={"background": "rgba(255,255,255,0.02)"},
                                ),
                                lg=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        dcc.Graph(id="distribution-chart", config={"displayModeBar": False})
                                    ),
                                    className="border-0 mb-4",
                                    style={"background": "rgba(255,255,255,0.02)"},
                                ),
                                lg=6,
                            ),
                        ]
                    ),
                    label="Comparative Analytics",
                    tab_id="tab-analytics",
                    tabClassName="text-light fw-semibold",
                    label_style={"padding": "12px 20px"},
                ),
                dbc.Tab(
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    dash_table.DataTable(
                                        id="datatable-interactivity",
                                        columns=[{"name": "Country", "id": "Country"}, {"name": "City", "id": "City"}],
                                        data=[],
                                        style_header={
                                            "backgroundColor": THEME_COLORS["primary"],
                                            "color": "white",
                                            "fontWeight": "bold",
                                            "border": "0px",
                                        },
                                        style_data={
                                            "backgroundColor": "rgba(255,255,255,0.92)",
                                            "color": THEME_COLORS["dark"],
                                            "border": "0px",
                                            "fontSize": "0.9rem",
                                        },
                                        style_data_conditional=[
                                            {"if": {"row_index": "odd"}, "backgroundColor": "rgba(246,247,249,0.7)"}
                                        ],
                                        page_size=12,
                                        filter_action="native",
                                        sort_action="native",
                                        sort_mode="multi",
                                        style_table={"overflowX": "auto"},
                                    )
                                ),
                                className="border-0",
                                style={"background": "rgba(255,255,255,0.02)"},
                            ),
                            width=12,
                        )
                    ),
                    label="City Catalogue",
                    tab_id="tab-table",
                    tabClassName="text-light fw-semibold",
                    label_style={"padding": "12px 20px"},
                ),
            ],
            id="main-tabs",
            active_tab="tab-map",
            className="mt-3",
        )

    def build_footer() -> dbc.Row:
        return dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Span(
                            [
                                html.I(className="fas fa-database me-2"),
                                "Data Source: ",
                                html.A(
                                    "Wikipedia – Greek Colonisation",
                                    href="https://en.wikipedia.org/wiki/Greek_colonisation",
                                    target="_blank",
                                    className="text-decoration-none text-info",
                                ),
                            ],
                            className="text-white-50",
                        )
                    ],
                    className="text-center py-3",
                ),
                width=12,
            ),
            className="mt-4",
        )

    # ------------------------------------------------------------------
    # Application layout
    # ------------------------------------------------------------------

    app.layout = dbc.Container(
        [
            dcc.Store(id="selected-country-store", data="ALL"),
            dcc.Store(id="filtered-records-store"),
            dcc.Download(id="download-filtered-data"),
            build_hero_banner(),
            build_metric_cards(),
            build_control_panel(),
            build_tabs(),
            build_footer(),
        ],
        fluid=True,
        className="px-3",
        style={"minHeight": "100vh", "color": "white"},
    )

    # ------------------------------------------------------------------
    # Plot generators
    # ------------------------------------------------------------------

    def filter_dataframe(
        base_df: pd.DataFrame,
        categories: Sequence[str],
        colony_range: Sequence[int],
    ) -> pd.DataFrame:
        filtered = base_df.copy()
        if categories:
            filtered = filtered[filtered["Category"].isin(categories)]
        if colony_range:
            start, end = int(colony_range[0]), int(colony_range[1])
            filtered = filtered[(filtered["No of Cities"] >= start) & (filtered["No of Cities"] <= end)]
        return filtered

    def generate_map(
        plot_df: pd.DataFrame,
        selected_country: str,
        projection: str,
        size_mode: str,
    ) -> go.Figure:
        if plot_df.empty:
            fig = go.Figure()
            fig.update_layout(
                geo={
                    "projection": {"type": projection or "natural earth"},
                    "bgcolor": "rgba(0,0,0,0)",
                },
                paper_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    {
                        "text": "No countries match the current filters",
                        "showarrow": False,
                        "font": {"size": 18, "color": "#ffffff"},
                    }
                ],
            )
            return fig

        plot_df = plot_df.copy()

        if size_mode == "uniform":
            plot_df["marker_size"] = 25
        else:
            plot_df["marker_size"] = plot_df["No of Cities"].astype(float) * 18

        plot_df["marker_opacity"] = 0.85
        if selected_country and selected_country != "ALL" and selected_country in plot_df["Country"].values:
            plot_df.loc[plot_df["Country"] != selected_country, "marker_opacity"] = 0.25
            plot_df.loc[plot_df["Country"] == selected_country, "marker_size"] *= 1.4

        fig = px.scatter_geo(
            plot_df,
            lon="Longitude",
            lat="Latitude",
            color="Category",
            size="marker_size",
            hover_name="Country",
            hover_data={"No of Cities": True, "marker_size": False},
            color_discrete_map=CATEGORY_COLORS,
            size_max=70,
            custom_data=["Country", "No of Cities"],
        )

        for trace in fig.data:
            trace.marker.line = dict(color="#FFFFFF", width=2)
            trace.marker.opacity = plot_df.loc[plot_df["Category"] == trace.name, "marker_opacity"].tolist()

        geo_config = dict(
            projection={"type": projection or "natural earth"},
            showland=True,
            landcolor=THEME_COLORS["sand"],
            showocean=True,
            oceancolor="rgba(12,31,45,0.8)",
            showcoastlines=True,
            coastlinecolor="#0F5C7E",
            coastlinewidth=1.5,
            showcountries=True,
            countrywidth=1,
            countrycolor="#8297A8",
            showframe=False,
            bgcolor="rgba(0,0,0,0)",
        )

        if selected_country and selected_country != "ALL" and selected_country in plot_df["Country"].values:
            country_data = plot_df.loc[plot_df["Country"] == selected_country].iloc[0]
            geo_config.update(
                center=dict(lon=float(country_data["Longitude"]), lat=float(country_data["Latitude"])),
                projection_scale=9 if projection == "orthographic" else 6,
            )
        else:
            geo_config.update(center=dict(lon=20, lat=40), projection_scale=3.4)

        fig.update_layout(
            title=dict(
                text=(
                    "<b style=\"font-family:Cinzel,serif;font-size:28px;\">Ancient Greek Colonies Distribution</b><br>"
                    "<span style=\"color:#B0C6D5;font-size:14px;\">Interact to explore colonisation intensity</span>"
                ),
                x=0.5,
                xanchor="center",
            ),
            geo=geo_config,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(10,23,35,0.9)",
                font=dict(color="#ECF0F1"),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=60, b=0),
        )

        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>Colonies: %{customdata[1]}<extra></extra>"
        )

        return fig

    def generate_top_countries_bar(plot_df: pd.DataFrame, selected_country: str) -> go.Figure:
        if plot_df.empty:
            fig = go.Figure()
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    {
                        "text": "No data available",
                        "showarrow": False,
                        "font": {"color": "white", "size": 16},
                    }
                ],
            )
            return fig

        df_sorted = plot_df.sort_values("No of Cities", ascending=True).tail(10)
        colors = []
        for country in df_sorted["Country"]:
            if selected_country != "ALL" and country == selected_country:
                colors.append(THEME_COLORS["accent"])
            else:
                colors.append(THEME_COLORS["secondary"])

        fig = go.Figure(
            data=
            [
                go.Bar(
                    y=df_sorted["Country"],
                    x=df_sorted["No of Cities"],
                    orientation="h",
                    marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.6)", width=1)),
                    text=df_sorted["No of Cities"],
                    textposition="outside",
                    customdata=df_sorted["Country"],
                    hovertemplate="<b>%{y}</b><br>Colonies: %{x}<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title=dict(text="<b>Top Host Regions</b>", x=0.5, font=dict(color="#ECF0F1")),
            xaxis_title="Colonies",
            yaxis_title="",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECF0F1"),
            margin=dict(l=10, r=30, t=50, b=10),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            hovermode="closest",
        )
        return fig

    def generate_category_distribution(plot_df: pd.DataFrame) -> go.Figure:
        if plot_df.empty:
            fig = go.Figure()
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    {
                        "text": "No data available",
                        "showarrow": False,
                        "font": {"color": "white", "size": 16},
                    }
                ],
            )
            return fig

        category_counts = plot_df.groupby("Category").size().reindex(CATEGORY_COLORS.keys(), fill_value=0)
        fig = go.Figure(
            data=[
                go.Bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    marker=dict(
                        color=[CATEGORY_COLORS.get(cat, THEME_COLORS["secondary"]) for cat in category_counts.index],
                        line=dict(color="rgba(255,255,255,0.6)", width=1),
                    ),
                    hovertemplate="%{x}<br>Countries: %{y}<extra></extra>",
                )
            ]
        )
        fig.update_layout(
            title=dict(text="<b>Distribution Across Colony Bands</b>", x=0.5, font=dict(color="#ECF0F1")),
            xaxis_title="Intensity Band",
            yaxis_title="Countries",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECF0F1"),
            margin=dict(l=20, r=20, t=50, b=40),
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        )
        return fig

    def generate_treemap(plot_df: pd.DataFrame) -> go.Figure:
        if plot_df.empty:
            fig = go.Figure()
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    {
                        "text": "Treemap unavailable",
                        "showarrow": False,
                        "font": {"color": "white", "size": 16},
                    }
                ],
            )
            return fig

        fig = px.treemap(
            plot_df,
            path=[px.Constant("Colonies"), "Category", "Country"],
            values="No of Cities",
            color="Category",
            color_discrete_map=CATEGORY_COLORS,
            custom_data=["Country", "No of Cities"],
        )
        fig.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>Colonies: %{customdata[1]}<extra></extra>",
            textinfo="label+percent entry",
        )
        fig.update_layout(
            title=dict(text="<b>Category Hierarchy</b>", x=0.5, font=dict(color="#ECF0F1")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=50, b=0),
        )
        return fig

    def generate_distribution_chart(plot_df: pd.DataFrame) -> go.Figure:
        if plot_df.empty:
            fig = go.Figure()
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=[
                    {
                        "text": "No distribution to display",
                        "showarrow": False,
                        "font": {"color": "white", "size": 16},
                    }
                ],
            )
            return fig

        sorted_counts = plot_df.sort_values("No of Cities", ascending=False)
        sorted_counts["Rank"] = range(1, len(sorted_counts) + 1)
        sorted_counts["Cumulative Share"] = sorted_counts["No of Cities"].cumsum() / sorted_counts["No of Cities"].sum()

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=sorted_counts["Rank"],
                y=sorted_counts["No of Cities"],
                mode="lines+markers",
                line=dict(color=THEME_COLORS["secondary"], width=3),
                marker=dict(size=8, color=THEME_COLORS["accent"]),
                hovertemplate="Rank %{x}: %{y} colonies<extra></extra>",
                name="Colonies",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=sorted_counts["Rank"],
                y=sorted_counts["Cumulative Share"],
                mode="lines",
                line=dict(color=THEME_COLORS["warning"], dash="dash"),
                yaxis="y2",
                name="Cumulative Share",
                hovertemplate="Rank %{x}: %{y:.0%} cumulative<extra></extra>",
            )
        )

        fig.update_layout(
            title=dict(text="<b>Colonies Concentration Curve</b>", x=0.5, font=dict(color="#ECF0F1")),
            xaxis_title="Ranked host regions",
            yaxis_title="Colonies",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ECF0F1"),
            margin=dict(l=50, r=50, t=50, b=40),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
            yaxis2=dict(
                overlaying="y",
                side="right",
                range=[0, 1],
                tickformat=",%",
                gridcolor="rgba(255,255,255,0)",
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        )
        return fig

    def generate_gauge(plot_df: pd.DataFrame, selected_country: str) -> go.Figure:
        fig = go.Figure()
        if plot_df.empty:
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            return fig

        if selected_country != "ALL" and selected_country in plot_df["Country"].values:
            row = plot_df.loc[plot_df["Country"] == selected_country].iloc[0]
            value = float(row["No of Cities"])
            subtitle = f"{selected_country}"
        else:
            value = float(plot_df["No of Cities"].mean())
            subtitle = "Average per filtered country"

        max_value = float(plot_df["No of Cities"].max())
        threshold = float(plot_df["No of Cities"].median())

        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=value,
                delta={"reference": threshold, "increasing": {"color": THEME_COLORS["success"]}},
                gauge={
                    "axis": {"range": [0, max(max_value * 1.1, 5)]},
                    "bar": {"color": THEME_COLORS["accent"]},
                    "steps": [
                        {"range": [0, threshold], "color": "rgba(42, 140, 203, 0.3)"},
                        {"range": [threshold, max_value], "color": "rgba(231, 126, 35, 0.3)"},
                    ],
                },
                title={"text": f"Colonisation Intensity\n<sub>{subtitle}</sub>", "font": {"color": "#ECF0F1"}},
                number={"font": {"color": "#ECF0F1"}},
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=30, r=30, t=80, b=30),
        )
        return fig

    def build_info_panel(
        filtered_df: pd.DataFrame,
        selected_country: str,
        total_cities_filtered: int,
        categories: Sequence[str],
        colony_range: Sequence[int],
    ) -> html.Div:
        if filtered_df.empty:
            return dbc.Alert(
                "No countries match the current combination of filters.",
                color="warning",
                className="mb-0",
            )

        if selected_country != "ALL" and selected_country in filtered_df["Country"].values:
            row = filtered_df.loc[filtered_df["Country"] == selected_country].iloc[0]
            body = [
                html.H5(selected_country, className="text-info fw-bold"),
                html.P(f"Colonies catalogued: {int(row['No of Cities'])}", className="mb-1"),
                html.P(f"Category: {row['Category']}", className="mb-1"),
                html.P(f"Share of filtered total: {row['No of Cities'] / filtered_df['No of Cities'].sum():.1%}", className="mb-1"),
                html.P(f"Current filters: {', '.join(categories)} | Range {colony_range[0]}-{colony_range[1]}", className="small text-muted"),
            ]
            return dbc.Alert(body, color="info", className="mb-0")

        top_row = filtered_df.loc[filtered_df["No of Cities"].idxmax()]
        body = [
            html.H5("Filtered Insights", className="text-info fw-bold"),
            html.P(f"Visible colonies: {total_cities_filtered}", className="mb-1"),
            html.P(f"Countries displayed: {filtered_df.shape[0]}", className="mb-1"),
            html.P(
                f"Leading region: {top_row['Country']} ({int(top_row['No of Cities'])} colonies)",
                className="mb-1",
            ),
            html.P(
                f"Filter bands: {', '.join(categories)} | Range {colony_range[0]}-{colony_range[1]}",
                className="small text-muted",
            ),
        ]
        return dbc.Alert(body, color="dark", className="mb-0")

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    @app.callback(
        Output("bubble-map", "figure"),
        Output("bar-chart", "figure"),
        Output("category-chart", "figure"),
        Output("treemap-chart", "figure"),
        Output("distribution-chart", "figure"),
        Output("datatable-interactivity", "data"),
        Output("datatable-interactivity", "columns"),
        Output("selected-info", "children"),
        Output("total-colonies-value", "children"),
        Output("total-countries-value", "children"),
        Output("avg-colonies-value", "children"),
        Output("top-country-name", "children"),
        Output("top-country-count", "children"),
        Output("selected-country-store", "data"),
        Output("filter-summary", "children"),
        Output("gauge-chart", "figure"),
        Output("filtered-records-store", "data"),
        Input("country-selector", "value"),
        Input("category-checklist", "value"),
        Input("colony-range-slider", "value"),
        Input("projection-selector", "value"),
        Input("marker-mode", "value"),
        Input("bubble-map", "clickData"),
        Input("bar-chart", "clickData"),
        Input("treemap-chart", "clickData"),
        Input("reset-button", "n_clicks"),
        State("selected-country-store", "data"),
    )
    def update_visualisations(
        dropdown_value,
        selected_categories,
        colony_range,
        projection_value,
        marker_mode,
        map_click,
        bar_click,
        treemap_click,
        reset_clicks,
        stored_selection,
    ):
        triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0] if dash.callback_context.triggered else None

        selected_country = stored_selection or "ALL"

        if triggered == "reset-button":
            selected_country = "ALL"
        elif triggered == "bubble-map" and map_click:
            selected_country = map_click["points"][0]["customdata"][0]
        elif triggered == "bar-chart" and bar_click:
            selected_country = bar_click["points"][0]["customdata"]
        elif triggered == "treemap-chart" and treemap_click:
            custom = treemap_click["points"][0].get("label")
            if custom in df["Country"].values:
                selected_country = custom
        elif triggered == "country-selector":
            selected_country = dropdown_value

        if not selected_categories:
            selected_categories = list(CATEGORY_COLORS.keys())

        filtered_df = filter_dataframe(df, selected_categories, colony_range)

        if selected_country not in filtered_df["Country"].values:
            selected_country = "ALL"

        map_fig = generate_map(filtered_df, selected_country, projection_value, marker_mode)
        bar_fig = generate_top_countries_bar(filtered_df, selected_country)
        category_fig = generate_category_distribution(filtered_df)
        treemap_fig = generate_treemap(filtered_df)
        distribution_fig = generate_distribution_chart(filtered_df)
        gauge_fig = generate_gauge(filtered_df, selected_country)

        if filtered_df.empty:
            filtered_cities = cities_df.iloc[0:0]
        elif selected_country != "ALL":
            filtered_cities = cities_df[cities_df["Country"] == selected_country]
        else:
            filtered_cities = cities_df[cities_df["Country"].isin(filtered_df["Country"])].copy()

        if selected_country == "ALL" or filtered_cities["Country"].nunique() > 1:
            table_columns = [{"name": "Country", "id": "Country"}, {"name": "City", "id": "City"}]
        else:
            table_columns = [{"name": "City", "id": "City"}]

        info_panel = build_info_panel(
            filtered_df,
            selected_country,
            int(filtered_df["No of Cities"].sum()) if not filtered_df.empty else 0,
            selected_categories,
            colony_range,
        )

        summary_text = (
            f"Active filters → Bands: {', '.join(selected_categories)} | "
            f"Colonies range: {colony_range[0]} - {colony_range[1]}"
        )

        total_colonies_display = (
            f"{filtered_df['No of Cities'].sum():.0f}" if not filtered_df.empty else str(total_colonies)
        )
        total_countries_display = (
            f"{filtered_df.shape[0]}" if not filtered_df.empty else str(total_countries)
        )
        avg_colonies_display = (
            f"{filtered_df['No of Cities'].mean():.1f}" if not filtered_df.empty else f"{avg_colonies:.1f}"
        )

        if not filtered_df.empty:
            top_row = filtered_df.loc[filtered_df["No of Cities"].idxmax()]
            top_country_name = str(top_row["Country"])
            top_country_count = f"{int(top_row['No of Cities'])} colonies"
        else:
            top_country_name = max_country
            top_country_count = f"{max_colonies} colonies"

        filtered_records = filtered_df.to_dict("records")

        return (
            map_fig,
            bar_fig,
            category_fig,
            treemap_fig,
            distribution_fig,
            filtered_cities.to_dict("records"),
            table_columns,
            info_panel,
            total_colonies_display,
            total_countries_display,
            avg_colonies_display,
            top_country_name,
            top_country_count,
            selected_country,
            summary_text,
            gauge_fig,
            filtered_records,
        )

    @app.callback(
        Output("download-filtered-data", "data"),
        Input("download-button", "n_clicks"),
        State("filtered-records-store", "data"),
        prevent_initial_call=True,
    )
    def download_filtered_data(n_clicks, records):
        if not records:
            return dash.no_update
        download_df = pd.DataFrame.from_records(records)
        return dcc.send_data_frame(download_df.to_csv, "ancient_greek_colonies_snapshot.csv", index=False)

    return app


if __name__ == "__main__":
    app = create_professional_app()
    print("=" * 70)
    print("🏛️  ANCIENT GREEK COLONISATION EXPLORER - PROFESSIONAL EDITION")
    print("=" * 70)
    print("\n✨ Highlights:")
    print("   • Cinematic Cyborg theme with glassmorphism overlays")
    print("   • Rich control centre featuring intensity sliders & projection toggles")
    print("   • Interactive storytelling panels reacting to every selection")
    print("   • Comparative analytics suite with treemap & Lorenz-style concentration curve")
    print("   • Downloadable filtered snapshot for offline exploration")
    print("\n🌐 Open your browser at: http://127.0.0.1:8050/")
    print("\n⌨️  Press Ctrl+C to stop the server")
    print("=" * 70)
    app.run(debug=False, port=8050)

