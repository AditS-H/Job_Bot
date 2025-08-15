from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from bs4 import BeautifulSoup
import re
import random

# User agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
]

def search_paid_internships(proxies, query="internship", location="us", max_results=100):
    jobs = []
    url = f"https://www.indeed.com/jobs?q={query}+paid&l={location}"
    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = random.choice(proxies) if proxies else None
    if proxy.http_proxy:
        options.add_argument(f'--proxy-server={proxy.http_proxy}')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        # Wait for Cloudflare (no paid CAPTCHA solver)
        time.sleep(random.uniform(5, 10))  # Wait for JS challenges
        if "checking your browser" in driver.page_source.lower():
            print("Cloudflare detected, waiting longer...")
            time.sleep(random.uniform(10, 15))  # Hope page loads
        
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 5))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.find_all('div', class_='job_seen_beacon')[:max_results]
        
        for card in job_cards:
            try:
                job_id = card.get('data-jk', '')
                title = card.find('h2', class_='jobTitle').text.strip() if card.find('h2', class_='jobTitle') else 'Internship'
                company = card.find('span', class_='companyName').text.strip() if card.find('span', class_='companyName') else 'Unknown'
                description = card.find('div', class_='job-snippet').text.strip() if card.find('div', class_='job-snippet') else ''
                job_url = 'https://www.indeed.com' + card.find('a')['href'] if card.find('a') else ''
                
                if is_paid_internship(description):
                    jobs.append({
                        'id': job_id,
                        'title': title,
                        'company': {'display_name': company},
                        'description': description,
                        'redirect_url': job_url
                    })
            except Exception as e:
                print(f"Error parsing job card: {e}")
        
        return jobs
    finally:
        driver.quit()

def is_paid_internship(description):
    description = description.lower()
    return ('paid' in description or 'stipend' in description or '$' in description) and \
           'unpaid' not in description and 'volunteer' not in description

def scrape_job_page(url, proxies):
    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = random.choice(proxies) if proxies else None
    if proxy.http_proxy:
        options.add_argument(f'--proxy-server={proxy.http_proxy}')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(random.uniform(5, 10))  # Wait for Cloudflare
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        email = None
        for a in soup.find_all('a', href=True):
            if 'mailto:' in a['href']:
                email = a['href'].replace('mailto:', '')
                break
        if not email:
            email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text)
            email = email.group(0) if email else None
        return email or f'hr@{url.split("/")[2].replace("www.", "").split(".")[0]}.com'
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return 'hr@company.com'
    finally:
        driver.quit()