import requests
from bs4 import BeautifulSoup
import csv
import config_data
import datetime

def scrape():
    # URL strony do pobrania
    type ='RPA'
    site= "nofluffjobs.com"
    url = f"https://{site}/pl/{type}"


    # Pobierz zawartość strony
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Nie udało się pobrać strony: {response.status_code}")
        exit()

    # Przetwarzanie HTML za pomocą BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # data = soup.find_all('div', class_='tw-flex tw-items-center')
    data = soup.find_all('a',href=True)

    dataTime=datetime.datetime.now()
    formatted_dataTime = dataTime.strftime("%Y-%m-%d %H:%M:%S")
    
    # Zapisz dane do pliku txt
    with open('output.csv', 'w',newline ='' ,encoding='utf-8') as file:
        writer = csv.writer(file)
        result =[]
        for element in data:
            h3_element = element.find('h3')
            if h3_element:
                job = h3_element.get_text(strip=True)
            else:
                job = 'Brak tytułu'  
            href=element['href']
            if href.startswith('/pl/job/'):  # Filtruj tylko ścieżki wewnętrzne
                full_url = f"https://nofluffjobs.com{href}"  # Uzupełnij URL
                writer.writerow([job,full_url,site,type,formatted_dataTime])  # Zapisz pełny link jako jedną linię
                result.append([job,full_url,site,type,formatted_dataTime])

    return result
            
scraped_data = scrape()
            

 


