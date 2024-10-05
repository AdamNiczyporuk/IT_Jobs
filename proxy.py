from stem import Signal
from stem.control import Controller
import config_data as config
import requests
import subprocess
import time 
import random
from fake_useragent import UserAgent


proxy_list=[
    'http://80.13.39.65:80',
    'http://211.73.79.129:80',
    'http://3.67.179.153:3128',
    # 'http://85.215.64.49:80',
    # 'http://188.152.75.218:80',
    'http://91.134.253.17:80',
    'http://23.88.51.178:8888',
    'http://164.92.164.95:80',
    'http://37.26.196.36:8081',
    'http://43.132.219.102:80',
    'http://102.213.146.206:8080',
    'http://51.91.109.83:80',
    'http://8.213.22.253:3128',
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
        # 'https': proxy
    }
    
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
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
    url = f"http://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start=0"
    response = make_request_proxy(url)  
    print(response.status_code)
    print(response.text)