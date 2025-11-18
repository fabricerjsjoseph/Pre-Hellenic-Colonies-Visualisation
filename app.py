"""Ancient Greek Colonization Chat Agent - Main Application

This is the main Chainlit application file that implements an agentic chat interface
for exploring Ancient Greek colonization data using OpenRouter LLMs.
"""

import json
from typing import Optional, Dict, List, Any
import pandas as pd
from openai import OpenAI

import chainlit as cl
from chainlit.input_widget import Select

import config
from GR03A_DataFrame import create_df_for_viz, txt_to_dataframe
from agent_tools import (
    compare_countries,
    generate_map_visualization,
    generate_bar_chart,
    generate_category_distribution,
)


# =============================================================================
# OpenRouter Client Setup
# =============================================================================

def get_openrouter_client() -> OpenAI:
    """Initialize and return OpenRouter client."""
    api_key = config.OPENROUTER_API_KEY
    
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. Please set it in your environment variables.\n"
            "Get your API key from: https://openrouter.ai/keys"
        )
    
    return OpenAI(
        base_url=config.OPENROUTER_BASE_URL,
        api_key=api_key,
        default_headers={
            "HTTP-Referer": config.OPENROUTER_SITE_URL,
            "X-Title": config.OPENROUTER_APP_NAME,
        }
    )


# =============================================================================
# Data Loading
# =============================================================================

def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and cache the colonization data."""
    df = create_df_for_viz()
    cities_df = txt_to_dataframe()
    return df, cities_df


# =============================================================================
# Agent System
# =============================================================================

def create_agent_context(df: pd.DataFrame, cities_df: pd.DataFrame) -> str:
    """Create context about the available data for the agent."""
    total_colonies = int(df["No of Cities"].sum())
    total_countries = len(df)
    top_country = df.loc[df["No of Cities"].idxmax()]
    
    context = f"""
=== DATA CONTEXT ===
You have access to a dataset of Ancient Greek colonies with the following information:

Total Colonies: {total_colonies}
Total Countries/Regions: {total_countries}
Most Colonized Region: {top_country['Country']} ({int(top_country['No of Cities'])} colonies)

Countries with most colonies:
{df.nlargest(5, 'No of Cities')[['Country', 'No of Cities']].to_string(index=False)}

You can help users by:
1. Answering questions about specific countries or regions
2. Providing statistics and comparisons
3. Generating visualizations (suggest when appropriate)
4. Explaining historical patterns

When a user asks for visualizations, respond with a JSON block in this format:
```json
{{
  "visualization": "map" | "bar" | "category" | "comparison",
  "parameters": {{
    "country": "Country Name" (optional),
    "countries": ["Country1", "Country2"] (for comparison),
    "projection": "natural earth" | "orthographic" | "mercator"
  }}
}}
```
"""
    return context


async def call_llm(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    stream: bool = True
) -> str:
    """Call the LLM via OpenRouter."""
    client = cl.user_session.get("openrouter_client")
    model = model or cl.user_session.get("model", config.DEFAULT_MODEL)
    model_config = config.AVAILABLE_MODELS.get(model, {})
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=model_config.get("max_tokens", config.DEFAULT_MAX_TOKENS),
            temperature=model_config.get("temperature", config.DEFAULT_TEMPERATURE),
            stream=stream,
        )
        
        if stream:
            msg = cl.Message(content="")
            await msg.send()
            
            full_response = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    await msg.stream_token(content)
            
            await msg.update()
            return full_response
        else:
            return response.choices[0].message.content
            
    except Exception as e:
        error_msg = f"Error calling LLM: {str(e)}"
        await cl.Message(content=f"❌ {error_msg}").send()
        raise


def extract_visualization_request(response: str) -> Optional[Dict[str, Any]]:
    """Extract visualization request from LLM response if present."""
    if "```json" in response:
        try:
            # Extract JSON block
            start = response.find("```json") + 7
            end = response.find("```", start)
            json_str = response[start:end].strip()
            viz_request = json.loads(json_str)
            
            if "visualization" in viz_request:
                return viz_request
        except (json.JSONDecodeError, ValueError):
            # If JSON parsing fails, return None to indicate no valid visualization request was found
            pass
    return None


# =============================================================================
# Chainlit Event Handlers
# =============================================================================

@cl.on_chat_start
async def start():
    """Initialize chat session."""
    # Load data
    df, cities_df = load_data()
    
    # Initialize OpenRouter client
    try:
        client = get_openrouter_client()
        cl.user_session.set("openrouter_client", client)
    except ValueError as e:
        await cl.Message(
            content=f"❌ **Configuration Error**\n\n{str(e)}\n\n"
            "Please set your OPENROUTER_API_KEY environment variable and restart the application."
        ).send()
        return
    
    # Store data in session
    cl.user_session.set("df", df)
    cl.user_session.set("cities_df", cities_df)
    cl.user_session.set("model", config.DEFAULT_MODEL)
    cl.user_session.set("chat_history", [])
    
    # Create agent context
    context = create_agent_context(df, cities_df)
    cl.user_session.set("agent_context", context)
    
    # Welcome message
    welcome_message = f"""# Welcome to the Ancient Greek Colonization Explorer! 🏛️

I'm your AI assistant for exploring Ancient Greek colonies across the Mediterranean during the Pre-Hellenic period.

## 📊 Dataset Overview
- **Total Colonies**: {int(df['No of Cities'].sum())}
- **Regions**: {len(df)} countries/regions
- **Top Region**: {df.loc[df['No of Cities'].idxmax()]['Country']} ({int(df.loc[df['No of Cities'].idxmax()]['No of Cities'])} colonies)

## 💬 What can I help you with?

**Ask questions like:**
- "Tell me about Greek colonies in Italy"
- "Which regions had the most colonies?"
- "Compare colonization in Turkey and Greece"
- "Show me a map of all colonies"
- "What patterns do you see in the colonization data?"

**Request visualizations:**
- Maps showing colony distribution
- Bar charts comparing regions
- Category breakdowns
- Statistical analysis

## ⚙️ Current Settings
- **Model**: {config.AVAILABLE_MODELS[config.DEFAULT_MODEL]['name']}

Feel free to ask me anything about Ancient Greek colonization!
"""
    
    await cl.Message(content=welcome_message).send()
    
    # Set up chat settings
    await cl.ChatSettings(
        [
            Select(
                id="model",
                label="LLM Model",
                values=list(config.AVAILABLE_MODELS.keys()),
                initial_value=config.DEFAULT_MODEL,
            ),
        ]
    ).send()


@cl.on_settings_update
async def settings_update(settings):
    """Handle settings updates."""
    model = settings.get("model")
    if model:
        cl.user_session.set("model", model)
        model_info = config.AVAILABLE_MODELS.get(model, {})
        await cl.Message(
            content=f"✅ Model changed to: **{model_info.get('name', model)}**\n\n"
            f"_{model_info.get('description', '')}_"
        ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    user_message = message.content
    
    # Get session data
    df = cl.user_session.get("df")
    cities_df = cl.user_session.get("cities_df")
    agent_context = cl.user_session.get("agent_context")
    chat_history = cl.user_session.get("chat_history", [])
    
    # Build messages for LLM
    messages = [
        {"role": "system", "content": config.AGENT_SYSTEM_PROMPT + "\n" + agent_context}
    ]
    
    # Add chat history (keep last N messages)
    messages.extend(chat_history[-config.MAX_CHAT_HISTORY:])
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    # Call LLM
    try:
        response = await call_llm(messages, stream=config.ENABLE_STREAMING)
        
        # Update chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": response})
        cl.user_session.set("chat_history", chat_history)
        
        # Check for visualization requests
        viz_request = extract_visualization_request(response)
        if viz_request:
            await generate_visualization(viz_request, df, cities_df)
            
    except Exception as e:
        await cl.Message(
            content=f"❌ An error occurred: {str(e)}\n\nPlease try again."
        ).send()


async def generate_visualization(viz_request: Dict[str, Any], df: pd.DataFrame, cities_df: pd.DataFrame):
    """Generate and send a visualization based on the request."""
    viz_type = viz_request.get("visualization")
    params = viz_request.get("parameters", {})
    
    try:
        if viz_type == "map":
            fig = generate_map_visualization(df, params)
            await cl.Message(
                content="📍 Here's the map visualization:",
                elements=[cl.Plotly(figure=fig, name="colony_map", display="inline")]
            ).send()
            
        elif viz_type == "bar":
            fig = generate_bar_chart(df, params)
            await cl.Message(
                content="📊 Here's the bar chart:",
                elements=[cl.Plotly(figure=fig, name="bar_chart", display="inline")]
            ).send()
            
        elif viz_type == "category":
            fig = generate_category_distribution(df, params)
            await cl.Message(
                content="📈 Here's the category distribution:",
                elements=[cl.Plotly(figure=fig, name="category_chart", display="inline")]
            ).send()
            
        elif viz_type == "comparison":
            countries = params.get("countries", [])
            if countries:
                comparison_data = compare_countries(df, cities_df, countries)
                await cl.Message(content=comparison_data).send()
                
    except Exception as e:
        await cl.Message(
            content=f"⚠️ Could not generate visualization: {str(e)}"
        ).send()


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    # This is just for reference - Chainlit apps are run with: chainlit run app.py
    print("To run this application, use: chainlit run app.py")
    print("Make sure OPENROUTER_API_KEY is set in your environment.")
