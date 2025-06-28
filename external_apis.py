import requests
import json

def check_google_safe_Browse(url_to_check, api_key):
    """
    Checks a URL against the Google Safe Browse API (Web Risk API).
    
    Args:
        url_to_check (str): The URL to check.
        api_key (str): Your Google Cloud API key.
        
    Returns:
        str: The status of the URL (e.g., 'CLEAN', 'MALWARE', 'SOCIAL_ENGINEERING').
    """
    api_url = f"https://webrisk.googleapis.com/v1/uris:search?key={api_key}"
    
    payload = {
        'uri': url_to_check,
        'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE']
    }
    
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (like 4xx or 5xx)
        
        data = response.json()
        
        # If the 'threat' key exists, a threat was found.
        if 'threat' in data:
            threat_type = data['threat'].get('threatTypes', ['UNKNOWN'])[0]
            print(f"  -> Google Safe Browse Alert: {threat_type}")
            return threat_type
        else:
            # If the key is not present, the URI is considered clean.
            return "CLEAN"
            
    except requests.exceptions.RequestException as e:
        print(f"  -> Could not check Google Safe Browse: {e}")
        return "CHECK_ERROR"