import argparse
from urllib.parse import urlparse
from domain_analysis import get_whois_info, get_dns_records, check_domain_similarity
from content_analysis import get_page_content, extract_metadata, take_screenshot
from reporting import generate_report
import validators

# In a real application, this would be a configurable list of critical sector entities.
TARGET_ORGANISATIONS = ["mybank.com", "government.gov", "criticalservice.org"]

def main():
    parser = argparse.ArgumentParser(description="Phishing Domain and Page Detector")
    parser.add_argument("url", help="The URL to analyze.")
    args = parser.parse_args()

    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    if not validators.url(url):
        print(f"Error: Invalid URL provided: {url}")
        return

    domain = urlparse(url).netloc

    print(f"Analyzing URL: {url}")
    print(f"Domain: {domain}")

    # --- Domain Analysis ---
    whois_info = get_whois_info(domain)
    dns_records = get_dns_records(domain)
    similar_domains = check_domain_similarity(domain, TARGET_ORGANISATIONS)

    # --- Web Content Analysis ---
    html_content = get_page_content(url)
    metadata = {}
    screenshot_path = ""
    content_error = False # Initialize our error flag

    if "Error" in html_content:
        content_error = True
    else:
        metadata = extract_metadata(html_content)
        screenshot_path = take_screenshot(url, domain)

    # --- Reporting ---
    generate_report(domain, whois_info, dns_records, similar_domains, metadata, screenshot_path, content_error)


if __name__ == "__main__":
    main()