import trafilatura
import logging
from typing import Any

# Configure logging
logger = logging.getLogger(__name__)

def visit_webpage(url: str) -> dict[str, Any]:
    """
    Visits a web page and extracts its main text content.
    
    Use this tool when:
    - You found an interesting URL from `search_google` and need to read the full article.
    - You need to analyze the details of a news report, a technical blog, or a documentation page.
    
    This tool filters out navigation bars, ads, and footers, returning only the main body text.
    
    Args:
        url: The full URL to visit (must start with http:// or https://).
        
    Returns:
        dict: {
            "status": "success" | "error",
            "title": "Page Title",
            "content": "Full extracted text content...",
            "original_url": "..."
        }
    """
    try:
        print(f"\n[DEBUG] Browsing URL: {url}") # Explicit Debug Log
        downloaded = trafilatura.fetch_url(url)
        
        if downloaded is None:
            return {
                "status": "error",
                "message": f"Failed to download content from {url}. The site might block bots or return empty content.",
                "original_url": url
            }

        text_content = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
        
        if not text_content:
             return {
                "status": "error",
                "message": "Downloaded page but failed to extract text. The page might be empty or purely JavaScript-based.",
                "original_url": url
            }

        # Simple metadata extraction just from the string download isn't perfect, 
        # but trafilatura.extract returns just the string.
        # For title, we'd ideally use bare_extraction, but extract is safer for now.
        
        return {
            "status": "success",
            "content": text_content[:10000],  # Limit to 10k chars to protect Context Window
            "note": "Content truncated to first 10000 characters if too long.",
            "original_url": url
        }

    except Exception as e:
        logger.error(f"Browse failed: {e}")
        return {
            "status": "error",
            "message": str(e),
            "original_url": url
        }
