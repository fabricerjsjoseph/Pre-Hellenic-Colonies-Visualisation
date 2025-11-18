# Ancient Greek Colonization Chat Agent 🏛️💬

An AI-powered conversational assistant for exploring Ancient Greek colonies across the Mediterranean during the Pre-Hellenic period. This agentic chat application combines historical data with modern LLMs through OpenRouter to provide an interactive, educational experience.

## 🌟 Features

### Agentic Chat Interface
- **Natural Language Queries**: Ask questions in plain English about Greek colonization
- **Context-Aware Responses**: AI maintains conversation history for coherent dialogue
- **Historical Expertise**: Deep knowledge of Pre-Hellenic period colonies and settlements
- **Interactive Visualizations**: Request maps, charts, and comparisons on demand

### Powered by OpenRouter
- **Multiple LLM Options**: Choose from various models (Claude, GPT-4, Llama, Gemini, etc.)
- **Flexible Configuration**: Easy model switching based on your needs and budget
- **Streaming Responses**: Real-time response generation for better UX

### Data Analysis Capabilities
The agent can:
- Answer questions about specific countries/regions
- Provide statistics and comparisons
- Generate visualizations (maps, bar charts, category distributions)
- Analyze patterns and trends in colonization
- Search for specific colonies or cities
- Compare multiple regions side-by-side

## 📊 Dataset

The application uses historical data on Ancient Greek colonies including:
- **475+ colonies** across the Mediterranean and Black Sea
- **30+ countries/regions** with Greek settlements
- Geographic coordinates for mapping
- Categorization by colonization intensity

Data source: [Wikipedia - Greek Colonisation](https://en.wikipedia.org/wiki/Greek_colonisation)

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/fabricerjsjoseph/Pre-Hellenic-Colonies-Visualisation.git
   cd Pre-Hellenic-Colonies-Visualisation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

4. **Run the chat application**
   ```bash
   chainlit run app.py
   ```

5. **Open your browser**
   
   The application will automatically open at `http://localhost:8000`

## 💬 Usage Examples

### Sample Questions

**Basic Information:**
- "Tell me about Greek colonies in Italy"
- "How many colonies did Turkey have?"
- "What were the main regions of Greek colonization?"

**Comparisons:**
- "Compare colonization in Turkey and Italy"
- "Which regions had more than 50 colonies?"
- "Show me the top 5 most colonized regions"

**Visualizations:**
- "Show me a map of all colonies"
- "Create a bar chart of the top 10 regions"
- "Display the category distribution"

**Analysis:**
- "What patterns do you see in the colonization data?"
- "Why did certain regions have more colonies?"
- "Explain the geographic distribution"

### Chat Interface

The chat interface includes:
- **Message Input**: Type your questions naturally
- **Model Selection**: Change LLM models in settings
- **Streaming Responses**: See answers appear in real-time
- **Inline Visualizations**: Charts and maps appear directly in chat
- **Chat History**: Context maintained throughout conversation

## ⚙️ Configuration

### LLM Models

The application supports multiple models through OpenRouter. Default configuration in `config.py`:

#### **Recommended Models:**

**Default: Claude 3.5 Sonnet** (Best for historical analysis)
```python
DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"
```
- Excellent reasoning for complex historical queries
- Strong context understanding
- Best for nuanced historical discussions

**Alternative Options:**

| Model | Use Case | Cost Tier |
|-------|----------|-----------|
| `openai/gpt-4-turbo-preview` | General purpose, broad knowledge | Premium |
| `anthropic/claude-3-haiku` | Fast, efficient for simple queries | Mid |
| `openai/gpt-3.5-turbo` | Cost-effective, quick responses | Mid |
| `meta-llama/llama-3.1-70b-instruct` | Open-source, budget-friendly | Budget |
| `google/gemini-pro` | Google's model, good balance | Budget |

### Customizing the Agent

Edit `config.py` to customize:

**Agent Behavior:**
```python
AGENT_SYSTEM_PROMPT = "Your custom system prompt..."
MAX_CHAT_HISTORY = 20  # Number of messages to keep
ENABLE_STREAMING = True  # Stream responses
```

**Visualization Settings:**
```python
DEFAULT_MAP_PROJECTION = "natural earth"
DEFAULT_COLOR_SCHEME = {...}
```

**Model Parameters:**
```python
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
```

## 🎨 Visualization Types

### 1. Geographic Maps
Interactive maps showing colony distribution with:
- Color-coded categories
- Bubble sizes based on colony count
- Multiple projection options
- Country highlighting

### 2. Bar Charts
Compare regions with:
- Top N countries
- Sorted by colony count
- Highlighted selections

### 3. Category Distributions
View intensity bands:
- 90+ colonies
- 60-90 colonies
- 30-60 colonies
- 10-20 colonies
- Less than 10 colonies

## 🏗️ Architecture

```
┌─────────────────┐
│   Chainlit UI   │  ← User Interface
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
┌────────▼────────┐  ┌────▼─────────┐
│   app.py        │  │  config.py   │
│  (Main Agent)   │  │  (Settings)  │
└────────┬────────┘  └──────────────┘
         │
         ├──────────────┬──────────────┐
         │              │              │
┌────────▼────────┐  ┌──▼────────┐  ┌─▼──────────┐
│  agent_tools.py │  │ OpenRouter│  │  Data CSV  │
│  (Utilities)    │  │    API    │  │   Files    │
└─────────────────┘  └───────────┘  └────────────┘
```

### Key Components:

- **app.py**: Main Chainlit application with chat logic
- **config.py**: Configuration for models, prompts, and settings
- **agent_tools.py**: Data analysis and visualization functions
- **GR03A_DataFrame.py**: Original data processing module

## 📂 Project Structure

```
Pre-Hellenic-Colonies-Visualisation/
├── app.py                          # Main chat application
├── config.py                       # Configuration settings
├── agent_tools.py                  # Agent utility functions
├── GR03A_DataFrame.py             # Data processing
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── README_CHAT_AGENT.md          # This file
├── README.md                      # Original Dash app README
│
├── Data files:
├── GR03-Ancient Greek Cities...txt
├── GR03-Country Code Mapping.csv
└── GR03-Selected Capital Geo...csv

├── Original Dash Applications:
├── GR03B_Greek_Colonies_Dashboard.py
├── GR03B_Greek_Colonies_Dashboard_Enhanced.py
└── GR03B_Greek_Colonies_Dashboard_Professional.py
```

## 🔐 Security & API Keys

### OpenRouter API Key
- Required for LLM access
- Store in `.env` file (never commit!)
- Get free key at [openrouter.ai](https://openrouter.ai)
- Supports pay-as-you-go pricing

### Best Practices:
- Never commit `.env` file
- Use `.env.example` for templates
- Rotate keys regularly
- Monitor usage on OpenRouter dashboard

## 🛠️ Development

### Running Original Dash Apps

The repository also includes the original Dash visualization apps:

```bash
# Professional version (recommended)
python GR03B_Greek_Colonies_Dashboard_Professional.py

# Enhanced version
python GR03B_Greek_Colonies_Dashboard_Enhanced.py

# Original version
python GR03B_Greek_Colonies_Dashboard.py
```

### Adding New Features

**To add new analysis capabilities:**
1. Add function to `agent_tools.py`
2. Update `AGENT_SYSTEM_PROMPT` in `config.py`
3. Handle in `generate_visualization()` in `app.py`

**To add new models:**
1. Add to `AVAILABLE_MODELS` in `config.py`
2. Test with your OpenRouter account

## 🐛 Troubleshooting

### Common Issues:

**"OPENROUTER_API_KEY not found"**
- Ensure `.env` file exists with valid API key
- Check environment variable is set: `echo $OPENROUTER_API_KEY`

**"No module named 'chainlit'"**
- Install dependencies: `pip install -r requirements.txt`

**Visualizations not appearing**
- Check browser console for errors
- Ensure Plotly is installed correctly

**Slow responses**
- Try a faster model (GPT-3.5, Claude Haiku)
- Check OpenRouter status
- Verify internet connection

## 📚 Learn More

### About the Technologies:
- **Chainlit**: [docs.chainlit.io](https://docs.chainlit.io)
- **OpenRouter**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **Plotly**: [plotly.com/python](https://plotly.com/python/)

### Historical Context:
- [Greek Colonisation - Wikipedia](https://en.wikipedia.org/wiki/Greek_colonisation)
- [Ancient Greek Colonies](https://www.worldhistory.org/Greek_Colonization/)

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional analysis features
- More visualization types
- Enhanced prompt engineering
- Multi-language support
- Voice input/output
- Export capabilities

## 📝 License

This project uses historical data from Wikipedia and is intended for educational purposes.

## 🙏 Acknowledgments

- Original data from [Wikipedia - Greek Colonisation](https://en.wikipedia.org/wiki/Greek_colonisation)
- Built with [Chainlit](https://chainlit.io)
- Powered by [OpenRouter](https://openrouter.ai)
- Visualizations with [Plotly](https://plotly.com)

---

**Note**: This chat agent complements the original Dash visualization apps. Both interfaces are available for different use cases - use the chat agent for conversational exploration and the Dash apps for comprehensive dashboards.
