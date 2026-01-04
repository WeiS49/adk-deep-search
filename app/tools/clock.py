from datetime import datetime

def get_current_time() -> dict[str, str]:
    """
    Returns the current local date and time.
    
    Use this tool when the user asks:
    - "What is the date today?"
    - "What time is it?"
    - Questions that require a temporal baseline (e.g., "How long ago was X?").
    
    Returns:
        dict: {
            "current_time": "YYYY-MM-DD HH:MM:SS Weekday",
            "status": "success"
        }
    """
    now = datetime.now()
    return {
        "status": "success",
        "current_time": now.strftime("%Y-%m-%d %H:%M:%S %A")
    }
