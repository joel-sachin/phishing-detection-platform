import requests
import re
from bs4 import BeautifulSoup
import logging

# Import our custom modules
from domain_analysis import check_domain_similarity, get_whois_info
from content_analysis import get_page_content, take_screenshot 
from database import add_alert
from external_apis import check_google_safe_Browse
from config import TARGET_ORGANISATIONS, PHISHING_KEYWORDS, GOOGLE_API_KEY

# Get the logger that is configured in app.py
logger = logging.getLogger(__name__)


def find_keywords_in_content(html_content):
    """Scans HTML content for a list of keywords and returns found keywords."""
    found_keywords = []
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(["script", "style"]):
        element.decompose()
    page_text = soup.get_text().lower()
    
    for keyword in PHISHING_KEYWORDS:
        if keyword in page_text:
            found_keywords.append(keyword)
    return found_keywords

def fetch_new_domains():
    """Fetches newly registered domains by monitoring Certificate Transparency logs."""
    logger.info("Fetching new domains from Certificate Transparency logs...")
    domains = set()
    try:
        response = requests.get("https://crt.sh/?q=%.com&output=json", timeout=30)
        response.raise_for_status()

        for cert in response.json():
            name = cert.get('common_name')
            if name and not name.startswith('*.'):
                root_domain_match = re.search(r'[^.]+\.[^.]+$', name)
                if root_domain_match:
                    domains.add(root_domain_match.group(0).lower())

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching domains from crt.sh: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during domain fetching: {e}")
        
    logger.info(f"Found {len(domains)} unique domains to analyze.")
    return domains

def run_monitoring_task():
    """The main function for the background monitoring task."""
    logger.info("Starting scheduled monitoring task...")
    new_domains = fetch_new_domains()
    
    if not new_domains:
        logger.info("No new domains to analyze in this run.")
        return

    for domain in new_domains:
        similar_domains = check_domain_similarity(domain, TARGET_ORGANISATIONS)
        if similar_domains:
            for target, score in similar_domains:
                logger.warning(f"Suspicious domain name found: {domain} (Similar to {target})")
                
                whois_info = get_whois_info(domain)
                creation_date_str = "N/A"
                if whois_info and whois_info.get('creation_date'):
                    creation_date = whois_info.get('creation_date')
                    if isinstance(creation_date, list):
                        creation_date = creation_date[0]
                    creation_date_str = creation_date.strftime('%Y-%m-%d')
                
                status = "Suspicious"
                found_keywords = []
                screenshot_file_path = ""
                url_to_check = 'http://' + domain
                html_content = get_page_content(url_to_check)

                if "Error" not in html_content:
                    logger.info(f"Successfully fetched content from {domain}")
                    found_keywords = find_keywords_in_content(html_content)
                    if found_keywords:
                        status = "High-Risk Phishing"
                        logger.warning(f"!! Found phishing keywords in {domain}: {found_keywords}")
                        
                        logger.info(f"Taking screenshot of {domain}...")
                        screenshot_file_path = take_screenshot(url_to_check, domain)
                        if "Error" in screenshot_file_path:
                            logger.error(f"Could not take screenshot for {domain}: {screenshot_file_path}")
                            screenshot_file_path = ""
                        else:
                            logger.info(f"Screenshot saved to {screenshot_file_path}")
                
                logger.info(f"Checking {domain} with Google Safe Browse...")
                gsb_status = check_google_safe_Browse(url_to_check, GOOGLE_API_KEY)
                
                if gsb_status not in ['CLEAN', 'CHECK_ERROR']:
                    status = "High-Risk Phishing"
                    logger.warning(f"Google Safe Browse confirmed threat for {domain}: {gsb_status}")

                add_alert(domain, target, score, creation_date_str, status, found_keywords, screenshot_file_path, gsb_status)
    
    logger.info("Scheduled monitoring task finished.")

def run_test_alert():
    """Simulates finding a High-Risk domain to test the full pipeline."""
    logger.info("Simulating a full HIGH-RISK domain alert for testing...")
    
    test_domain = "my-apple-secure-test.com"
    target_organisation = "apple.com"
    score = 94
    creation_date = "2025-06-28"
    status = "High-Risk Phishing"
    keywords = ["login", "apple", "secure"]
    screenshot_path = "" # Leave blank for test, as no file is actually created
    gsb_status = "SOCIAL_ENGINEERING"

    logger.info(f"Adding test alert for '{test_domain}'")
    # Call add_alert with all 8 arguments
    add_alert(test_domain, target_organisation, score, creation_date, status, keywords, screenshot_path, gsb_status)
    return f"Test alert for '{test_domain}' has been successfully added."