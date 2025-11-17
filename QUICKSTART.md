# Quick Start Guide - Ancient Greek Colonization Chat Agent

This guide will help you get started with the AI-powered chat agent in just a few minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- OpenRouter API key (free tier available)

## Step-by-Step Setup

### 1. Get Your OpenRouter API Key

1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Go to [Keys](https://openrouter.ai/keys)
4. Create a new API key
5. Copy your API key (you'll need it in step 3)

**Note**: OpenRouter offers free tier credits and pay-as-you-go pricing. Most models cost $0.001-0.02 per 1K tokens.

### 2. Install Dependencies

Open a terminal and navigate to the project directory:

```bash
cd Pre-Hellenic-Colonies-Visualisation
pip install -r requirements.txt
```

This will install:
- Chainlit (chat interface)
- OpenAI SDK (API client)
- Plotly (visualizations)
- Pandas (data processing)
- Python-dotenv (environment variables)

### 3. Configure Your API Key

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenRouter API key:

```
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here
```

**Important**: Never commit the `.env` file to git! It's already in `.gitignore`.

### 4. Run the Chat Agent

Start the application:

```bash
chainlit run app.py
```

You should see:
```
Chainlit is running on http://localhost:8000
```

Your browser should automatically open to the chat interface!

## First Steps in the Chat

Once the app is running, try these example queries:

### 1. Get an Overview
```
Tell me about the Ancient Greek colonization data available
```

### 2. Ask About Specific Regions
```
How many colonies did Turkey have?
```

### 3. Request Comparisons
```
Compare Greek colonization in Italy and Greece
```

### 4. Generate Visualizations
```
Show me a map of all the colonies
```

### 5. Analyze Patterns
```
What patterns do you see in the colonization data?
```

## Changing the LLM Model

To change which AI model powers the chat:

1. Click the **Settings** icon in the chat interface
2. Select a different model from the dropdown:
   - **Claude 3.5 Sonnet** (Default, best reasoning)
   - **GPT-4 Turbo** (General purpose)
   - **Llama 3.1 70B** (Budget-friendly)
   - **Gemini Pro** (Google's model)

Each model has different strengths and pricing.

## Understanding the Response Format

The agent can provide several types of responses:

### Text Responses
Plain text with historical information, statistics, and insights.

### Markdown Tables
Formatted comparisons and data summaries:
```
| Country | Colonies | Category |
|---------|----------|----------|
| Turkey  | 98       | 90+      |
```

### Interactive Visualizations
- **Maps**: Geographic distribution of colonies
- **Bar Charts**: Top regions by colony count
- **Category Charts**: Distribution across intensity bands

## Troubleshooting

### "OPENROUTER_API_KEY not found"

**Solution**: Make sure you've created a `.env` file with your API key.

```bash
# Check if .env exists
ls -la .env

# If not, create it from template
cp .env.example .env
# Then edit .env with your API key
```

### Port 8000 Already in Use

**Solution**: Specify a different port:

```bash
chainlit run app.py --port 8001
```

### Slow Responses

**Solutions**:
1. Switch to a faster model (Claude Haiku or GPT-3.5)
2. Check your internet connection
3. Verify OpenRouter service status

### Import Errors

**Solution**: Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

- Read the full documentation in [README_CHAT_AGENT.md](README_CHAT_AGENT.md)
- Explore the configuration options in `config.py`
- Try the original Dash dashboards:
  ```bash
  python GR03B_Greek_Colonies_Dashboard_Professional.py
  ```

## Tips for Best Results

1. **Be Specific**: Instead of "Tell me about colonies", try "How many colonies were in the Black Sea region?"

2. **Request Visualizations**: The agent can generate charts and maps - just ask!

3. **Compare and Analyze**: Ask for comparisons between regions or analysis of patterns.

4. **Follow-up Questions**: The agent maintains context, so you can ask follow-up questions.

5. **Try Different Models**: Different models have different strengths - experiment to find what works best for your queries.

## Example Conversation

```
You: Tell me about Greek colonies in Turkey

Agent: Turkey was the most heavily colonized region by ancient Greeks, 
with 98 recorded colonies. This represents about 32% of all Greek 
colonies in the dataset...

You: Compare that to Italy

Agent: Let me compare Turkey and Italy for you:

| Country | Colonies | Category    |
|---------|----------|-------------|
| Turkey  | 98       | 90+         |
| Italy   | 65       | 60-90       |

Turkey had significantly more colonies (98) compared to Italy (65)...

You: Show me these on a map

Agent: [Generates interactive map showing both regions highlighted]
```

## Getting Help

- **Documentation**: See [README_CHAT_AGENT.md](README_CHAT_AGENT.md)
- **Issues**: Check the GitHub repository issues
- **OpenRouter**: Visit [openrouter.ai/docs](https://openrouter.ai/docs)

## Cost Estimates

Using OpenRouter with the default Claude 3.5 Sonnet model:
- Average query: ~500-1000 tokens
- Cost: ~$0.003-0.015 per query
- With $5 credit: 300-1500 queries

Budget models (Llama, Gemini) can be 10-50x cheaper!

Happy exploring! 🏛️
