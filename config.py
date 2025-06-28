import configparser

# Create a parser object
config = configparser.ConfigParser()

# Read the config.ini file
config.read('config.ini')

# --- Read Settings ---
SCHEDULER_INTERVAL = config.getint('SETTINGS', 'scheduler_interval_minutes', fallback=10)

# --- Read API Keys ---
GOOGLE_API_KEY = config.get('API_KEYS', 'google_api_key', fallback='YOUR_API_KEY_HERE')

# --- Read Lists ---
# The lists are multi-line, so we split them by newline and filter out empty lines.
target_orgs_str = config.get('TARGETS', 'organisations', fallback='')
TARGET_ORGANISATIONS = [line.strip() for line in target_orgs_str.strip().split('\n') if line.strip()]

phishing_keywords_str = config.get('KEYWORDS', 'phishing_keywords', fallback='')
PHISHING_KEYWORDS = [line.strip() for line in phishing_keywords_str.strip().split('\n') if line.strip()]

# --- Sanity Check (optional but good practice) ---
if not TARGET_ORGANISATIONS:
    print("WARNING: No target organisations found in config.ini")
if GOOGLE_API_KEY == 'YOUR_API_KEY_HERE':
    print("WARNING: Google API key not set in config.ini")