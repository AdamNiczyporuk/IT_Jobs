from fake_useragent import UserAgent

ua = UserAgent()

def get_random_agent(): 
    return ua.random

