# Ancient Greek Colonies Visualisation 🏛️

## Description

An enhanced, interactive web application built with Dash to visualize ancient Greek colonies across the Mediterranean during the Pre-Hellenic period (before Philip II of Macedon). This application provides rich, interactive features for exploring historical settlement patterns with modern data visualization techniques.

The dataset came from: https://en.wikipedia.org/wiki/Greek_colonisation

## ✨ Features

### Enhanced Visualization (GR03B_Greek_Colonies_Dashboard_Enhanced.py)

**Interactive Components:**
- 📊 **Summary Statistics Dashboard** - Real-time stats showing total colonies, countries, averages, and top colonizer
- 🗺️ **Enhanced Bubble Map** - Interactive geographical visualization with:
  - Country highlighting on selection
  - Custom color-coded categories
  - Rich hover tooltips
  - Zoom, pan, and reset controls
- 📈 **Top 10 Countries Bar Chart** - Horizontal bar chart with gradient colors
- 🥧 **Category Distribution Pie Chart** - Visual breakdown of colony ranges
- 🔍 **Advanced Search & Filter** - Real-time search through colony names
- 📋 **Interactive Data Table** - Sortable, filterable colony listings with pagination

**Design Improvements:**
- Modern, responsive layout with clean UI
- Professional color scheme with high contrast
- Card-based statistics display
- Smooth interactions and transitions
- Emoji icons for visual appeal
- Consistent spacing and typography

**User Experience:**
- Country selection dropdown with highlighting
- Reset view button for quick navigation
- Dynamic info panel showing selected country details
- Integrated search functionality
- Mobile-friendly responsive design

## Demo

Watch longer demo on Youtube: https://youtu.be/shfUQK9v7Aw

### Original Version
![](Dash-Greek-Colonisation-20200204.gif)

### Enhanced Version Screenshots
![Enhanced Dashboard Overview](https://github.com/user-attachments/assets/7a864b4f-2283-4a25-bdc2-828ba327ee35)
*Overview showing all colonies with statistics cards, multiple charts, and interactive controls*

![Interactive Country Selection](https://github.com/user-attachments/assets/9f810e8d-6ade-492d-bf54-cd2369b38a9d)
*Greece selected showing filtered data, updated statistics, and highlighted map markers*

## 🚀 Getting Started

### Installation

1. Clone this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

**Enhanced Version (Recommended):**
```bash
python GR03B_Greek_Colonies_Dashboard_Enhanced.py
```

**Original Version:**
```bash
python GR03B_Greek_Colonies_Dashboard.py
```

Then open your browser to: http://127.0.0.1:8050/

## 📁 Project Structure

- **GR03A_DataFrame.py** - Data processing and wrangling module
- **GR03B_Greek_Colonies_Dashboard.py** - Original dashboard (updated for modern Dash)
- **GR03B_Greek_Colonies_Dashboard_Enhanced.py** - Enhanced dashboard with advanced features
- **GR03-Ancient Greek Cities Before Hellenistic Period 20200131.txt** - Source data
- **GR03-Country Code Mapping.csv** - Country code to name mapping
- **GR03-Selected Capital Geo Coordinates Modified.csv** - Geographical coordinates
- **requirements.txt** - Python dependencies

## 🛠️ Technical Details

### Data Processing Pipeline

1. **Data Extraction** - Raw data extracted from Wikipedia and stored in text format
2. **Data Wrangling** - GR03A_DataFrame.py processes the text data:
   - Parses colony codes and names using regex
   - Maps country codes to full country names
   - Assigns geographical coordinates
   - Categorizes countries by colony count
3. **Visualization** - Dashboard applications render interactive visualizations

### Technologies Used

- **Dash** - Web application framework
- **Plotly** - Interactive graphing library
- **Pandas** - Data manipulation and analysis
- **Python 3.12+** - Core programming language

### Key Improvements in Enhanced Version

- ✅ Modern Dash API (updated from deprecated components)
- ✅ Responsive card-based layout
- ✅ Multiple coordinated visualizations
- ✅ Real-time filtering and search
- ✅ Enhanced color schemes and styling
- ✅ Interactive country highlighting
- ✅ Summary statistics dashboard
- ✅ Professional UI/UX design
- ✅ Better error handling
- ✅ Improved code organization

## 📊 Data Categories

Colonies are categorized into 5 ranges:
- **90+ colonies** - Major colonization centers (e.g., Turkey: 98)
- **60-90 colonies** - Significant presence (e.g., Italy: 65)
- **30-60 colonies** - Moderate presence (e.g., Greece: 34)
- **10-20 colonies** - Minor presence (e.g., Albania: 15)
- **Less than 10 colonies** - Limited presence

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project uses historical data from Wikipedia and is intended for educational purposes.

## 🙏 Acknowledgments

- Data source: [Wikipedia - Greek Colonisation](https://en.wikipedia.org/wiki/Greek_colonisation)
- Built with Dash by Plotly
