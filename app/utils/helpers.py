from datetime import datetime

def parse_date(date_str):
    """Convert YYYY-MM-DD string to date object, or return None."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None