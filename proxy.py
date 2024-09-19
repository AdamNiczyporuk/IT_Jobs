from stem import Signal
from stem.control import Controller
import config_data as config
import requests
import subprocess
import time 
import agents as ag
import random


proxy_list=[
    'http://77.83.246.25:80',
    'http://80.13.39.65:80',
    'http://211.73.79.129:80',
]

def get_random_proxy():
    return random.choice(proxy_list)


def start_tor():
    subprocess.Popen(['D:\\Program Files\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe', '-f', 'D:\\Program Files\\Tor Browser\\Browser\\TorBrowser\\Data\\Tor\\torrc'])
    time.sleep(5)
    
def get_current_ip(session):
    response = session.get('https://api.ipify.org?format=json')
    return response.json()['ip']
    
def renew_ip(session): 
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=config.torPassword)  # Użyj zwykłego hasła tekstowego
        controller.signal(Signal.NEWNYM)
        print("renew ip")

    
        
def make_request_proxy(url):
    session = requests.Session()
    # Tor Proxies 
    # session.proxies = {
    #     'http': 'socks5h://127.0.0.1:9050',
    #     'https': 'socks5h://127.0.0.1:9050'
    # }
    
    proxy=get_random_proxy()
    print(proxy)
    session.proxies = {
        'http': proxy,
        'https': proxy
    }
    
    headers = {'User-Agent': ag.get_random_agent()}
    
    # renew_ip(session)
    
    try:
        response = session.get(url, headers=headers, timeout=60)
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

if __name__ == "__main__":
    # start_tor()
    tittle = "RPA"
    location = "Poland"
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start=0"
    response = make_request_proxy(url)  
    print(response.status_code)
    print(response.text)