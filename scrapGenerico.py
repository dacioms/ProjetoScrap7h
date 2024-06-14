# https://github.com/dacioms/ProjetoScrap7h.git



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuração do Selenium
def configure_selenium():
    options = Options()
    options.add_argument("--headless")  # Executa o navegador em modo headless (sem GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=Service("/path/to/chromedriver"), options=options)
    return driver

# Função para fazer scraping da página
def scrape_page(url, driver):
    driver.get(url)
    time.sleep(random.uniform(3, 7))  # Delay aleatório para simular comportamento humano
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')

# Função para obter proxies
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxies = []
    for row in soup.find('table', id='proxylisttable').tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].text,
            'port': row.find_all('td')[1].text
        })
    return proxies

# Função para usar proxies em requisições
def fetch_url_with_proxy(url, proxies):
    for proxy in proxies:
        try:
            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
            response = requests.get(url, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
            if response.status_code == 200:
                return response.text
        except:
            continue
    return None


# Função principal de scraping
base_url = "https://www.example.com/jobs"


def main_scraping():
    driver = configure_selenium()
    proxies = get_proxies()
    response_text = fetch_url_with_proxy(base_url, proxies)
    print("Texto do get proxy: ", response_text)
    soup = scrape_page(base_url, driver)
    jobs = []
    driver.quit()
    return jobs

if __name__ == "__main__":
    jobs = main_scraping()
    df = pd.DataFrame(jobs)
    df.to_json("jobs.json", index=False)
    print("Scraping concluído com sucesso!")