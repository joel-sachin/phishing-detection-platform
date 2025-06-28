import whois
import dns.resolver
import validators
from thefuzz import fuzz

def get_whois_info(domain):
    """
    Retrieves WHOIS information for a given domain.

    Args:
        domain (str): The domain name to query.

    Returns:
        dict: A dictionary containing WHOIS information, or an error message.
    """
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return {"error": f"Could not retrieve WHOIS information. The domain may not exist or there was a query error."}

def get_dns_records(domain):
    """
    Retrieves DNS records for a given domain.

    Args:
        domain (str): The domain name to query.

    Returns:
        dict: A dictionary containing various DNS records, or an error message.
    """
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [answer.to_text() for answer in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            records[record_type] = []
        except Exception as e:
            records[record_type] = [f"Error retrieving {record_type} record: {e}"]
    return records

def check_domain_similarity(domain, target_domains, threshold=85):
    """
    Checks domain similarity using Levenshtein distance via thefuzz library.
    Uses partial_ratio to find substrings.

    Args:
        domain (str): The domain to check.
        target_domains (list): A list of legitimate domains to compare against.
        threshold (int): The similarity score required to be considered a match (0-100).

    Returns:
        list: A list of tuples, where each tuple contains the similar target
              domain and the similarity score.
    """
    similar_domains = []
    domain_name_only = domain.split('.')[0]

    for target in target_domains:
        target_name_only = target.split('.')[0]
        # CHANGE HERE: Use partial_ratio for better substring matching.
        similarity_score = fuzz.partial_ratio(domain_name_only, target_name_only)

        if similarity_score >= threshold:
            similar_domains.append((target, similarity_score))

    return similar_domains