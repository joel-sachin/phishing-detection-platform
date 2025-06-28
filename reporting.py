def generate_report(domain, whois_info, dns_records, similar_domains, metadata, screenshot_path, content_error=False):
    """
    Generates a formatted report string of the analysis.

    Args:
        domain (str): The analyzed domain.
        whois_info (dict): WHOIS information.
        dns_records (dict): DNS records.
        similar_domains (list): List of tuples with (similar_target, score).
        metadata (dict): Webpage metadata.
        screenshot_path (str): Path to the webpage screenshot.
        content_error (bool): Flag indicating if there was an error fetching web content.
    
    Returns:
        str: A formatted report.
    """
    # Use a list to build the report parts and then join them. This is efficient.
    report_parts = []

    report_parts.append("="*50)
    report_parts.append(f"Analysis Report for: {domain}")
    report_parts.append("="*50 + "\n")

    report_parts.append("\n--- Domain Analysis ---")
    if "error" in whois_info:
        report_parts.append(f"WHOIS Information: {whois_info['error']}")
    else:
        report_parts.append("WHOIS Information:")
        keys_to_show = ['domain_name', 'registrar', 'creation_date', 'expiration_date', 'name_servers']
        for key, value in whois_info.items():
            if key in keys_to_show:
                report_parts.append(f"  {str(key).capitalize()}: {value}")

    report_parts.append("\nDNS Records:")
    for record_type, records in dns_records.items():
        report_parts.append(f"  {record_type}:")
        if records:
            for record in records:
                report_parts.append(f"    - {record}")
        else:
            report_parts.append("    - No records found")

    report_parts.append("\nDomain Similarity:")
    if similar_domains:
        report_parts.append("  Suspicious similarity found with the following target domains:")
        for target, score in similar_domains:
            report_parts.append(f"    - Similar to '{target}' with a score of {score}%")
    else:
        report_parts.append("  The domain does not show strong similarity to any target domains.")

    report_parts.append("\n--- Web Content Analysis ---")
    if content_error:
        report_parts.append("Could not access the webpage. The domain may not have a live website.")
    else:
        report_parts.append("Metadata:")
        for key, value in metadata.items():
            report_parts.append(f"  {key.capitalize()}: {value}")
        report_parts.append(f"\nScreenshot saved to: {screenshot_path}")

    # Join all the parts with a newline character to create the final string
    return "\n".join(report_parts)