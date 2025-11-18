#!/usr/bin/env python3
"""
Example script demonstrating the core functionality of the chat agent
without requiring Chainlit to be running.

This script shows how the agent tools work and what kind of analysis
can be performed on the Greek colonization data.
"""

from GR03A_DataFrame import create_df_for_viz, txt_to_dataframe
from agent_tools import (
    get_colony_statistics,
    get_country_details,
    search_colonies,
    compare_countries,
    generate_map_visualization,
    generate_bar_chart,
    generate_category_distribution,
    get_regional_analysis,
)


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def main():
    """Run example queries to demonstrate agent capabilities."""
    
    print_header("Ancient Greek Colonization Chat Agent - Demo")
    print("\nLoading data...")
    
    # Load data
    df = create_df_for_viz()
    cities_df = txt_to_dataframe()
    cities_df = cities_df.rename(columns={"Country Name": "Country", "City Name": "City"})
    
    print(f"✅ Loaded data for {len(df)} countries and {len(cities_df)} cities")
    
    # ==========================================================================
    # Example 1: Get Overall Statistics
    # ==========================================================================
    print_header("Example 1: Overall Statistics")
    
    stats = get_colony_statistics(df)
    print(f"\nTotal Colonies: {stats['total_colonies']}")
    print(f"Total Countries: {stats['total_countries']}")
    print(f"Average per Country: {stats['average_colonies']:.1f}")
    print(f"Median: {stats['median_colonies']:.0f}")
    
    print("\n📊 Top 5 Countries:")
    for item in stats['top_5_countries']:
        print(f"  • {item['Country']}: {item['No of Cities']} colonies")
    
    print("\n📈 Category Distribution:")
    for category, count in stats['category_distribution'].items():
        print(f"  • {category}: {count} countries")
    
    # ==========================================================================
    # Example 2: Country Details
    # ==========================================================================
    print_header("Example 2: Country Details - Turkey")
    
    country = "Turkey"
    details = get_country_details(df, cities_df, country)
    
    if details:
        print(f"\n🏛️ {details['country']}")
        print(f"  Colonies: {details['num_colonies']}")
        print(f"  Category: {details['category']}")
        print(f"  Location: {details['latitude']:.2f}°N, {details['longitude']:.2f}°E")
        print(f"  Total Cities in Dataset: {details['total_cities']}")
        print(f"\n  Sample Cities:")
        for city in details['cities'][:5]:
            print(f"    • {city}")
    
    # ==========================================================================
    # Example 3: Search Colonies
    # ==========================================================================
    print_header("Example 3: Search Colonies - 'Apollonia'")
    
    results = search_colonies(cities_df, "Apollonia")
    print(f"\nFound {len(results)} matches:")
    for i, result in enumerate(results[:10], 1):
        print(f"  {i}. {result['City']} ({result['Country']})")
    
    # ==========================================================================
    # Example 4: Compare Countries
    # ==========================================================================
    print_header("Example 4: Compare Countries")
    
    countries_to_compare = ["Turkey", "Italy", "Greece"]
    comparison = compare_countries(df, cities_df, countries_to_compare)
    print(comparison)
    
    # ==========================================================================
    # Example 5: Regional Analysis
    # ==========================================================================
    print_header("Example 5: Regional Analysis")
    
    analysis = get_regional_analysis(df)
    print(analysis)
    
    # ==========================================================================
    # Example 6: Visualization Generation
    # ==========================================================================
    print_header("Example 6: Visualization Generation")
    
    print("\n📍 Generating visualizations...")
    print("  • Map visualization: generate_map_visualization()")
    print("  • Bar chart: generate_bar_chart()")
    print("  • Category distribution: generate_category_distribution()")
    
    # Generate but don't display (would require browser)
    try:
        generate_map_visualization(df, {"projection": "natural earth"})
        generate_bar_chart(df, {"top_n": 10})
        generate_category_distribution(df, {})
        print("\n✅ All visualizations generated successfully!")
        print("   (In the chat app, these would be displayed inline)")
    except Exception as e:
        print(f"\n⚠️ Visualization generation: {e}")
    
    # ==========================================================================
    # Example 7: Category Breakdown
    # ==========================================================================
    print_header("Example 7: Colony Intensity Categories")
    
    categories = [
        "90+ colonies",
        "60 - 90 colonies",
        "30 - 60 colonies",
        "10 - 20 colonies",
        "Less than 10 colonies"
    ]
    
    print("\nColonies by Intensity Band:")
    for category in categories:
        countries = df[df['Category'] == category]['Country'].tolist()
        if countries:
            print(f"\n📌 {category}: {len(countries)} countries")
            for country in countries:
                num_colonies = df[df['Country'] == country]['No of Cities'].iloc[0]
                print(f"  • {country}: {num_colonies}")
    
    # ==========================================================================
    # Example 8: Geographic Distribution
    # ==========================================================================
    print_header("Example 8: Geographic Distribution")
    
    print("\nColonies by Region (approximate):")
    
    # Asia Minor / Anatolia
    asia_minor = ["Turkey"]
    asia_minor_colonies = df[df['Country'].isin(asia_minor)]['No of Cities'].sum()
    
    # Southern Italy & Sicily
    italy_region = ["Italy"]
    italy_colonies = df[df['Country'].isin(italy_region)]['No of Cities'].sum()
    
    # Greece and nearby
    greece_region = ["Greece", "Albania"]
    greece_colonies = df[df['Country'].isin(greece_region)]['No of Cities'].sum()
    
    # Black Sea
    black_sea = ["Ukraine", "Bulgaria", "Romania", "Russia"]
    black_sea_colonies = df[df['Country'].isin(black_sea)]['No of Cities'].sum()
    
    print(f"  • Asia Minor (Turkey): {asia_minor_colonies}")
    print(f"  • Italy: {italy_colonies}")
    print(f"  • Greece Region: {greece_colonies}")
    print(f"  • Black Sea: {black_sea_colonies}")
    
    # ==========================================================================
    # Summary
    # ==========================================================================
    print_header("Chat Agent Capabilities Summary")
    
    print("""
The Ancient Greek Colonization Chat Agent can:

✅ Answer natural language questions about the data
✅ Provide detailed statistics and summaries
✅ Compare multiple countries or regions
✅ Search for specific colonies or cities
✅ Generate interactive visualizations (maps, charts)
✅ Analyze patterns and trends
✅ Provide historical context and insights

To use the chat interface:
1. Set your OPENROUTER_API_KEY in .env
2. Run: chainlit run app.py
3. Ask questions in natural language!

Example questions:
  • "Which region had the most Greek colonies?"
  • "Compare colonization in Turkey and Italy"
  • "Show me a map of all colonies"
  • "What cities were named Apollonia?"
  • "What patterns do you see in the colonization?"
    """)
    
    print("=" * 70)


if __name__ == "__main__":
    main()
