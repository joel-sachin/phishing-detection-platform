import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def get_page_content(url):
    """
    Fetches the HTML content of a webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The HTML content, or an error message.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching page content: {e}"

def extract_metadata(html_content):
    """
    Extracts metadata from the HTML content of a webpage.

    Args:
        html_content (str): The HTML content.

    Returns:
        dict: A dictionary containing metadata.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {
        "title": soup.title.string if soup.title else "No title found",
        "description": "",
        "keywords": ""
    }
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        metadata["description"] = description.get('content')

    keywords = soup.find('meta', attrs={'name': 'keywords'})
    if keywords:
        metadata["keywords"] = keywords.get('content')

    return metadata

def take_screenshot(url, domain):
    """
    Takes a screenshot of a webpage.
    Args:
        url (str): The URL of the webpage.
        domain (str): The domain name to use for the screenshot filename.
    Returns:
        str: The path to the saved screenshot, or an error message.
    """
    try:
        options = Options()
        # --- Add these crucial arguments for running in Docker ---
        options.add_argument('--headless')
        options.add_argument('--no-sandbox') # Essential for running as root in Docker
        options.add_argument('--disable-dev-shm-usage') # Overcomes limited resource problems
        options.add_argument('--disable-gpu')
        options.add_argument("window-size=1280,800")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        screenshot_path = os.path.join('screenshots', f'{domain}.png')
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return screenshot_path
    except Exception as e:
        # Also quit the driver on error to prevent zombie processes
        if 'driver' in locals():
            driver.quit()
        return f"Error taking screenshot: {e}"
