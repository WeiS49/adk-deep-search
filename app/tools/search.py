import os
import logging
from typing import Any
from googleapiclient.discovery import build # type: ignore

# Configure logging
logger = logging.getLogger(__name__)

def search_google(query: str, num_results: int = 5) -> dict[str, Any]:
    """
    Performs a Google Search using the Custom Search JSON API.
    
    Use this tool when the user asks for:
    - Current events (news, weather, sports scores).
    - Factual information not contained in your training data.
    - Specialized knowledge that requires verifying external sources.
    
    This tool DOES NOT browse the content of the pages; it only returns the
    search result snippets (titles, links, and brief descriptions).
    
    Args:
        query: The search string to send to Google. Try to make this specific.
               Example: "current CEO of Google", "weather in Tokyo".
        num_results: Number of results to return. Default is 5, max is 10.
                     Use fewer results for faster response. more for more accurate results.
               
    Returns:
        A dictionary containing:
        - status: "success" or "error"
        - query: The original query used
        - results: A list of search results (title, link, snippet)
        - total_results: Estimated total number of results
        
    Raises:
        ValueError: If API keys are missing.
    """
    api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
    cse_id = os.environ.get("GOOGLE_SEARCH_CX")

    if not api_key or not cse_id:
        return {
            "status": "error",
            "message": "Missing Service Configuration. Environment variables GOOGLE_SEARCH_API_KEY or GOOGLE_SEARCH_CX are not set."
        }

    try:
        print(f"\n[DEBUG] Searching Google for: {query}")  # Explicit Debug Log
        service = build("customsearch", "v1", developerKey=api_key)
        
        # Execute the search
        res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()
        
        items = res.get("items", [])
        print(f"[DEBUG] Found {len(items)} results.") # Explicit Debug Log
        clean_results = []
        
        for item in items:
            clean_results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
            
        return {
            "status": "success",
            "query": query,
            "count": len(clean_results),
            "results": clean_results
        }
        
    except Exception as e:
        logger.error(f"Google Search failed: {e}")
        return {
            "status": "error",
            "query": query,
            "message": str(e)
        }
