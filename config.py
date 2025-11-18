"""Configuration file for the Ancient Greek Colonization Chat Agent

This module contains configuration settings for the agentic chat application,
including OpenRouter API settings and LLM model configurations.
"""

import os

# =============================================================================
# OpenRouter Configuration
# =============================================================================

# OpenRouter API settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Site information for OpenRouter (optional, used for rankings)
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "https://github.com/fabricerjsjoseph/Pre-Hellenic-Colonies-Visualisation")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "Ancient Greek Colonization Explorer")

# =============================================================================
# LLM Model Configuration
# =============================================================================

# Default model - Anthropic Claude 3.5 Sonnet (recommended for historical analysis)
# - Excellent reasoning capabilities for complex historical queries
# - Strong understanding of context and nuance
# - Good at generating structured responses
DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"

# Alternative models with different characteristics
AVAILABLE_MODELS = {
    # Premium models - Best performance
    "anthropic/claude-3.5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "description": "Best for complex historical analysis and reasoning",
        "max_tokens": 8192,
        "temperature": 0.7,
        "cost_tier": "premium",
    },
    "openai/gpt-4-turbo-preview": {
        "name": "GPT-4 Turbo",
        "description": "Excellent general-purpose model with broad knowledge",
        "max_tokens": 4096,
        "temperature": 0.7,
        "cost_tier": "premium",
    },
    
    # Mid-tier models - Good balance of performance and cost
    "anthropic/claude-3-haiku": {
        "name": "Claude 3 Haiku",
        "description": "Fast and efficient for straightforward queries",
        "max_tokens": 4096,
        "temperature": 0.7,
        "cost_tier": "mid",
    },
    "openai/gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "description": "Fast and cost-effective for common tasks",
        "max_tokens": 4096,
        "temperature": 0.7,
        "cost_tier": "mid",
    },
    
    # Budget models - Cost-effective
    "meta-llama/llama-3.1-70b-instruct": {
        "name": "Llama 3.1 70B",
        "description": "Open-source model, good performance at lower cost",
        "max_tokens": 4096,
        "temperature": 0.7,
        "cost_tier": "budget",
    },
    "google/gemini-pro": {
        "name": "Gemini Pro",
        "description": "Google's model, good for general tasks",
        "max_tokens": 4096,
        "temperature": 0.7,
        "cost_tier": "budget",
    },
}

# Model parameters
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7

# =============================================================================
# Agent Configuration
# =============================================================================

# Agent system prompt
AGENT_SYSTEM_PROMPT = """You are an expert historian and data visualization specialist with deep knowledge of Ancient Greek colonization during the Pre-Hellenic period (before Philip II of Macedon).

Your role is to help users explore and understand the historical data about Greek colonies across the Mediterranean. You have access to detailed information about:
- Greek colonies and settlements across different regions
- Number of colonies per country/region
- Geographical distribution of settlements
- Historical patterns and trends

You can:
1. Answer questions about Greek colonization history
2. Provide insights about specific countries or regions
3. Generate visualizations (maps, charts, tables) on demand
4. Analyze patterns and trends in the data
5. Compare different regions and their colonization intensity

When responding:
- Be informative and educational
- Provide historical context when relevant
- Suggest visualizations that might help understand the data
- Be precise with numbers and facts from the dataset
- If you're not certain about something, acknowledge it

Available data includes colonies in regions like Turkey (98 colonies), Italy (65), Greece (34), and many others across the Mediterranean and Black Sea regions."""

# Chat settings
MAX_CHAT_HISTORY = 20  # Number of messages to keep in context
ENABLE_STREAMING = True  # Stream responses for better UX

# =============================================================================
# Visualization Configuration
# =============================================================================

# Default visualization settings
DEFAULT_MAP_PROJECTION = "natural earth"
DEFAULT_COLOR_SCHEME = {
    "primary": "#1E2A38",
    "secondary": "#2A8CCB",
    "accent": "#E67E22",
    "success": "#27AE60",
}

# Plotly configuration
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "scrollZoom": True,
    "displaylogo": False,
}

# =============================================================================
# Application Settings
# =============================================================================

# Chainlit settings
APP_NAME = "Ancient Greek Colonization Explorer 🏛️"
APP_DESCRIPTION = "An AI-powered assistant for exploring Ancient Greek colonies across the Mediterranean"

# Feature flags
ENABLE_DATA_EXPORT = True
ENABLE_VOICE_INPUT = False  # Future feature
ENABLE_IMAGE_GENERATION = False  # Future feature

# =============================================================================
# Data Paths
# =============================================================================

DATA_FILE = "GR03-Ancient Greek Cities Before Hellenistic Period 20200131.txt"
COUNTRY_MAPPING_FILE = "GR03-Country Code Mapping.csv"
GEO_COORDINATES_FILE = "GR03-Selected Capital Geo Coordinates Modified.csv"
