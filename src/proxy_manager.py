import requests
from bs4 import BeautifulSoup

def get_free_proxies():
    try:
        url = "https://free-proxy-list.net/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.find('table').find_all('tr')[1:50]:  # Top 50 proxies
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text
                port = cols[1].text
                proxies.append(f'http://{ip}:{port}')
        return proxies if proxies else ['']  # Fallback to no proxy
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return ['']