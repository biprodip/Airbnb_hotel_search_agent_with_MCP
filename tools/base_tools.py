"""Custom LangChain tools for web search and weather lookup."""

import os

from langchain.tools import tool
import ollama
import requests


@tool
def web_search(query: str):
    """Perform a live web search using Ollama Cloud Web Search API for real-time information and news.

    Args:
        query: Search query string.

    Returns:
        List of top search results (max 2).
    """
    response = ollama.web_search(query=query, max_results=2)
    return response.results


@tool
def get_weather(location: str):
    """Get current weather for a location using WeatherAPI.com.

    Use for queries about weather, temperature, or conditions in any city.
    Examples: "weather in Paris", "temperature in Tokyo", "is it raining in London"

    Args:
        location: City name (e.g., "New York", "London", "Tokyo").

    Returns:
        Current weather information including temperature and conditions.
    """
    url = (
        f"http://api.weatherapi.com/v1/current.json"
        f"?key={os.getenv('WEATHER_API_KEY')}&q={location}&aqi=no"
    )

    response = requests.get(url=url, timeout=10)
    response.raise_for_status()

    return response.json()
