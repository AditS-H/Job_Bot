import time
import random
from scraper import search_paid_internships, scrape_job_page
from emailer import send_email
from cover_letter import generate_cover_letter
from db import init_db, check_application, log_application
from proxy_manager import get_free_proxies
from google_auth_oauthlib.flow import InstalledAppFlow

def run_autobot():
    # Initialize database
    conn, cursor = init_db()
    
    # Authenticate Gmail API
    creds = InstalledAppFlow.from_client_secrets_file(
        '../config/credentials.json', ['https://www.googleapis.com/auth/gmail.send']
    ).run_local_server(port=0)
    
    # Get free proxies
    proxies = get_free_proxies()
    
    # Search paid internships
    internships = search_paid_internships(proxies=proxies, max_results=100)
    
    for job in internships:
        job_id = job.get('id')
        company = job.get('company', {}).get('display_name', 'Unknown')
        job_title = job.get('title', 'Internship')
        description = job.get('description', '')
        job_url = job.get('redirect_url', '')
        
        # Check if already applied
        if check_application(cursor, job_id):
            continue
        
        # Scrape job page for contact email
        contact_email = scrape_job_page(job_url, proxies)
        
        # Generate tailored cover letter
        cover_letter = generate_cover_letter(company, job_title, description)
        
        # Send email
        try:
            send_email(contact_email, f"Application for {job_title} at {company}", cover_letter, creds)
            log_application(cursor, conn, job_id, company, contact_email, 'Sent')
            print(f"Applied to {job_title} at {company}")
            time.sleep(random.uniform(2, 5))  # Longer delay to avoid detection
        except Exception as e:
            print(f"Error applying to {job_title}: {e}")
            log_application(cursor, conn, job_id, company, contact_email, 'Failed')
    
    conn.close()

if __name__ == "__main__":
    run_autobot()