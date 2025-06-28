from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from urllib.parse import urlparse
import validators
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Import the logger setup function
from logger_setup import setup_logger

from domain_analysis import check_domain_similarity, get_whois_info, get_dns_records
from content_analysis import get_page_content, extract_metadata, take_screenshot
from reporting import generate_report
from database import get_all_alerts
# Make sure to import the test function
from monitor import run_monitoring_task, run_test_alert
from config import TARGET_ORGANISATIONS, SCHEDULER_INTERVAL

# --- Initialize the Logger ---
setup_logger()
logger = logging.getLogger(__name__)


app = Flask(__name__)


# --- On-Demand Analyzer Page ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        if not validators.url(url):
            return render_template('index.html', report="Error: Invalid URL provided.")
        domain = urlparse(url).netloc
        
        whois_info = get_whois_info(domain)
        dns_records = get_dns_records(domain)
        similar_domains = check_domain_similarity(domain, TARGET_ORGANISATIONS)
        html_content = get_page_content(url)
        metadata = {}
        screenshot_path = ""
        content_error = False
        if "Error" in html_content:
            content_error = True
        else:
            metadata = extract_metadata(html_content)
            screenshot_path = take_screenshot(url, domain)
        report_str = generate_report(domain, whois_info, dns_records, similar_domains, metadata, screenshot_path, content_error)
        return render_template('index.html', report=report_str)
    return render_template('index.html', report=None)


# --- Alerts Dashboard Page ---
@app.route('/dashboard')
def dashboard():
    # This is the line that was missing
    alerts = get_all_alerts()
    return render_template('dashboard.html', alerts=alerts)


# --- Route to trigger a test alert ---
@app.route('/test-alert')
def test_alert():
    message = run_test_alert()
    return redirect(url_for('dashboard'))


# --- Route to serve screenshot files ---
@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    return send_from_directory('screenshots', filename)


# --- Scheduler Setup ---
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(run_monitoring_task, 'interval', minutes=SCHEDULER_INTERVAL)
scheduler.start()
logger.info(f"Scheduler started. Monitoring task will run every {SCHEDULER_INTERVAL} minutes.")


if __name__ == '__main__':
    logger.info("Starting Flask application.")
    app.run(debug=False)