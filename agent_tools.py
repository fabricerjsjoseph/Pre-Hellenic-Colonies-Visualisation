"""Agent Tools for Ancient Greek Colonization Explorer

This module contains utility functions that the agent can use to analyze data
and generate visualizations.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import config


# =============================================================================
# Data Analysis Tools
# =============================================================================

def get_colony_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Get overall statistics about colonies."""
    stats = {
        "total_colonies": int(df["No of Cities"].sum()),
        "total_countries": len(df),
        "average_colonies": float(df["No of Cities"].mean()),
        "median_colonies": float(df["No of Cities"].median()),
        "max_colonies": int(df["No of Cities"].max()),
        "min_colonies": int(df["No of Cities"].min()),
    }
    
    # Top 5 countries
    top_5 = df.nlargest(5, "No of Cities")[["Country", "No of Cities"]].to_dict("records")
    stats["top_5_countries"] = top_5
    
    # Category distribution
    category_dist = df["Category"].value_counts().to_dict()
    stats["category_distribution"] = category_dist
    
    return stats


def get_country_details(df: pd.DataFrame, cities_df: pd.DataFrame, country: str) -> Optional[Dict[str, Any]]:
    """Get detailed information about a specific country."""
    country_data = df[df["Country"] == country]
    
    if country_data.empty:
        return None
    
    country_row = country_data.iloc[0]
    
    # Get list of cities - handle both column name formats
    country_col = "Country" if "Country" in cities_df.columns else "Country Name"
    city_col = "City" if "City" in cities_df.columns else "City Name"
    
    cities = cities_df[cities_df[country_col] == country][city_col].tolist()
    
    details = {
        "country": country,
        "num_colonies": int(country_row["No of Cities"]),
        "category": country_row["Category"],
        "latitude": float(country_row["Latitude"]),
        "longitude": float(country_row["Longitude"]),
        "cities": cities[:10],  # First 10 cities
        "total_cities": len(cities),
    }
    
    return details


def search_colonies(cities_df: pd.DataFrame, query: str) -> List[Dict[str, str]]:
    """Search for colonies by name."""
    # Handle both column name formats
    country_col = "Country" if "Country" in cities_df.columns else "Country Name"
    city_col = "City" if "City" in cities_df.columns else "City Name"
    
    # Case-insensitive search
    mask = cities_df[city_col].str.contains(query, case=False, na=False)
    results = cities_df[mask][[country_col, city_col]].head(20)
    
    # Rename columns to standard format for output
    results = results.rename(columns={country_col: "Country", city_col: "City"})
    
    return results.to_dict("records")


def compare_countries(df: pd.DataFrame, cities_df: pd.DataFrame, countries: List[str]) -> str:
    """Compare multiple countries side by side."""
    comparison_data = []
    
    for country in countries:
        details = get_country_details(df, cities_df, country)
        if details:
            comparison_data.append(details)
    
    if not comparison_data:
        return "No data found for the specified countries."
    
    # Create comparison table
    comparison = "## Country Comparison\n\n"
    comparison += "| Country | Colonies | Category | Sample Cities |\n"
    comparison += "|---------|----------|----------|---------------|\n"
    
    for data in comparison_data:
        cities_str = ", ".join(data["cities"][:3])
        comparison += f"| {data['country']} | {data['num_colonies']} | {data['category']} | {cities_str}... |\n"
    
    return comparison


# =============================================================================
# Visualization Tools
# =============================================================================

def generate_map_visualization(
    df: pd.DataFrame, 
    params: Dict[str, Any]
) -> go.Figure:
    """Generate a map visualization of colonies."""
    selected_country = params.get("country")
    projection = params.get("projection", "natural earth")
    
    plot_df = df.copy()
    
    # Add marker sizes
    plot_df["marker_size"] = plot_df["No of Cities"] * 15
    
    # Adjust opacity if country is selected
    plot_df["marker_opacity"] = 0.85
    if selected_country and selected_country in plot_df["Country"].values:
        plot_df.loc[plot_df["Country"] != selected_country, "marker_opacity"] = 0.25
        plot_df.loc[plot_df["Country"] == selected_country, "marker_size"] *= 1.5
    
    # Create the map
    fig = px.scatter_geo(
        plot_df,
        lon="Longitude",
        lat="Latitude",
        color="Category",
        size="marker_size",
        hover_name="Country",
        hover_data={"No of Cities": True, "marker_size": False},
        color_discrete_map={
            "90+ colonies": "#C0392B",
            "60 - 90 colonies": "#E67E22",
            "30 - 60 colonies": "#F1C40F",
            "10 - 20 colonies": "#27AE60",
            "Less than 10 colonies": "#2980B9",
        },
        size_max=50,
        projection=projection,
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="<b>Ancient Greek Colonies Distribution</b>",
            x=0.5,
            xanchor="center",
        ),
        geo=dict(
            projection={"type": projection},
            showland=True,
            landcolor="#E8D3A5",
            showocean=True,
            oceancolor="#5DADE2",
            showcoastlines=True,
            coastlinecolor="#0F5C7E",
        ),
        margin=dict(l=0, r=0, t=60, b=0),
        height=600,
    )
    
    # Apply opacity
    for trace in fig.data:
        trace.marker.opacity = plot_df.loc[plot_df["Category"] == trace.name, "marker_opacity"].tolist()
    
    return fig


def generate_bar_chart(
    df: pd.DataFrame,
    params: Dict[str, Any]
) -> go.Figure:
    """Generate a bar chart of top countries."""
    top_n = params.get("top_n", 10)
    selected_country = params.get("country")
    
    # Get top N countries
    df_sorted = df.nlargest(top_n, "No of Cities")
    
    # Color bars
    colors = []
    for country in df_sorted["Country"]:
        if selected_country and country == selected_country:
            colors.append("#E67E22")
        else:
            colors.append("#2A8CCB")
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=df_sorted["Country"],
                y=df_sorted["No of Cities"],
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(255,255,255,0.6)", width=1)
                ),
                text=df_sorted["No of Cities"],
                textposition="outside",
            )
        ]
    )
    
    fig.update_layout(
        title=f"<b>Top {top_n} Regions by Colony Count</b>",
        xaxis_title="Country/Region",
        yaxis_title="Number of Colonies",
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        xaxis=dict(tickangle=-45),
    )
    
    return fig


def generate_category_distribution(
    df: pd.DataFrame,
    params: Dict[str, Any]
) -> go.Figure:
    """Generate a category distribution chart."""
    category_order = [
        "90+ colonies",
        "60 - 90 colonies", 
        "30 - 60 colonies",
        "10 - 20 colonies",
        "Less than 10 colonies"
    ]
    
    category_colors = {
        "90+ colonies": "#C0392B",
        "60 - 90 colonies": "#E67E22",
        "30 - 60 colonies": "#F1C40F",
        "10 - 20 colonies": "#27AE60",
        "Less than 10 colonies": "#2980B9",
    }
    
    category_counts = df.groupby("Category").size().reindex(category_order, fill_value=0)
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=category_counts.index,
                y=category_counts.values,
                marker=dict(
                    color=[category_colors[cat] for cat in category_counts.index],
                    line=dict(color="rgba(255,255,255,0.6)", width=1),
                ),
                text=category_counts.values,
                textposition="outside",
            )
        ]
    )
    
    fig.update_layout(
        title="<b>Distribution Across Colony Intensity Bands</b>",
        xaxis_title="Colony Range",
        yaxis_title="Number of Countries",
        height=500,
        margin=dict(l=50, r=50, t=80, b=120),
        xaxis=dict(tickangle=-45),
    )
    
    return fig


def generate_comparison_chart(
    df: pd.DataFrame,
    countries: List[str]
) -> go.Figure:
    """Generate a comparison chart for specific countries."""
    comparison_df = df[df["Country"].isin(countries)]
    
    fig = go.Figure(
        data=[
            go.Bar(
                x=comparison_df["Country"],
                y=comparison_df["No of Cities"],
                marker=dict(
                    color="#2A8CCB",
                    line=dict(color="rgba(255,255,255,0.6)", width=1)
                ),
                text=comparison_df["No of Cities"],
                textposition="outside",
            )
        ]
    )
    
    fig.update_layout(
        title="<b>Country Comparison</b>",
        xaxis_title="Country",
        yaxis_title="Number of Colonies",
        height=400,
    )
    
    return fig


def get_regional_analysis(df: pd.DataFrame) -> str:
    """Generate a regional analysis summary."""
    total_colonies = int(df["No of Cities"].sum())
    
    analysis = "## Regional Analysis\n\n"
    
    # Top regions
    top_3 = df.nlargest(3, "No of Cities")
    analysis += "### Top 3 Regions:\n"
    for _, row in top_3.iterrows():
        percentage = (row["No of Cities"] / total_colonies) * 100
        analysis += f"- **{row['Country']}**: {int(row['No of Cities'])} colonies ({percentage:.1f}% of total)\n"
    
    # Category breakdown
    analysis += "\n### By Intensity:\n"
    for category in df["Category"].unique():
        count = len(df[df["Category"] == category])
        analysis += f"- **{category}**: {count} regions\n"
    
    # Geographic spread
    analysis += f"\n### Geographic Spread:\n"
    analysis += f"- Total regions with colonies: {len(df)}\n"
    analysis += f"- Average colonies per region: {df['No of Cities'].mean():.1f}\n"
    analysis += f"- Median colonies per region: {df['No of Cities'].median():.0f}\n"
    
    return analysis
