from stem import Signal
from stem.control import Controller
import config_data as config
import requests

def renew_ip(): 
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password=config.torPassword)  # Użyj zwykłego hasła tekstowego
        controller.signal(Signal.NEWNYM)
        print("renew ip")
        
def make_request_proxy(url):
    renew_ip()
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    response = session.get(url)
    return response

tittle = "RPA"
location = "Poland"
url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={tittle}&location={location}&start=0"
response = make_request_proxy(url)  
print(response.status_code)