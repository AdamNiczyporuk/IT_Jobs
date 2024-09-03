import requests
from bs4 import BeautifulSoup
import csv

# URL strony do pobrania
url = "https://nofluffjobs.com/pl/RPA"

# Pobierz zawartość strony
response = requests.get(url)
if response.status_code != 200:
    print(f"Nie udało się pobrać strony: {response.status_code}")
    exit()

# Przetwarzanie HTML za pomocą BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
# data = soup.find_all('div', class_='tw-flex tw-items-center')
data = soup.find_all('a',href=True)


# Zapisz dane do pliku txt
with open('output.csv', 'w',newline ='' ,encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job','link'])
    for element in data:
        h3_element = element.find('h3')
        if h3_element:
            job = h3_element.get_text(strip=True)
        else:
            job = 'Brak tytułu'  
        href=element['href']
        if href.startswith('/pl/job/'):  # Filtruj tylko ścieżki wewnętrzne
            full_url = f"https://nofluffjobs.com{href}"  # Uzupełnij URL
            writer.writerow([job,full_url])  # Zapisz pełny link jako jedną linię
           
            

            

 


