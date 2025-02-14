import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import init, Fore, Style
from tqdm import tqdm
import os
import time
import pyfiglet


init(autoreset=True)

def fetch_proxies_from_geonode(soup):
    proxies = []
    rows = soup.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 8:
            proxy = f"{cols[0].text}:{cols[1].text}"
            proxies.append(proxy)
    return proxies

def fetch_proxies_from_proxyscrape(response):
    proxy_list = response.text.strip().split('\r\n')
    return proxy_list

def fetch_proxies_from_sslproxies_or_free_proxy_list(soup):
    proxies = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            proxy = f"{cols[0].text}:{cols[1].text}"
            proxies.append(proxy)
    return proxies

def fetch_proxies_from_advanced_name(soup):
    proxies_text = soup.get_text()
    proxy_list = proxies_text.split('\n')
    return proxy_list

def fetch_proxies_from_other_sources(soup):
    proxies = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            proxy = f"{cols[0].text.strip()}:{cols[1].text.strip()}"
            proxies.append(proxy)
    return proxies

def fetch_proxies_from_echolink(soup):
    proxies = []
    rows = soup.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 5 and cols[4].text.strip() == 'Ready':
            proxy = f"{cols[1].text.strip()}:{cols[2].text.strip()}"
            proxies.append(proxy)
    return proxies

def fetch_proxies(url, print_sample=False):
    proxies = []
    domain = urlparse(url).netloc

    print(Fore.YELLOW + f"\nFetching proxies from {domain}...\n")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'geonode.com' in url:
            proxies = fetch_proxies_from_geonode(soup)
        elif 'proxyscrape.com' in url:
            proxies = fetch_proxies_from_proxyscrape(response)
        elif any(site in url for site in ['sslproxies.org', 'free-proxy-list.net']):
            proxies = fetch_proxies_from_sslproxies_or_free_proxy_list(soup)
        elif 'advanced.name' in url:
            proxies = fetch_proxies_from_advanced_name(soup)
        elif any(site in url for site in ['freeproxy.world', 'iplocation.net', '2ip.io', 'hidemy.life', 'freeproxylist.cc']):
            proxies = fetch_proxies_from_other_sources(soup)
        elif 'echolink.org' in url:
            proxies = fetch_proxies_from_echolink(soup)

        print(Fore.GREEN + f"\nFetched {len(proxies)} proxies from {domain}.\n")

        if print_sample and len(proxies) > 5:
            print(Fore.CYAN + "Sample of 5 proxies:")
            for proxy in proxies[:5]:
                print(proxy)
            print()
            print(Fore.YELLOW + Style.BRIGHT + "\nLoading..")

        time.sleep(0.5)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Failed to fetch proxies from {domain}: {e}")

    return domain, proxies

def write_proxies_to_file(proxy_dict):
    with open('proxies.txt', 'w') as f:
        for domain, proxies in proxy_dict.items():
            f.write(f"Proxies from {domain}\n")
            for proxy in proxies:
                f.write(proxy + '\n')
            f.write('\n')

def run_proxy_scraper():
    os.system('cls' if os.name == 'nt' else 'clear') 

    print(Fore.YELLOW + Style.BRIGHT + pyfiglet.figlet_format("Proxy Scraper"))
    print(Fore.CYAN + Style.BRIGHT + "Made by: github.com/cr0mb/\n")

    urls = [
        'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text',
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net',
        'https://advanced.name/freeproxy/667e4f3871c2f',
        'https://www.freeproxy.world/?country=US',
        'https://www.echolink.org/proxylist.jsp',
        'https://www.iplocation.net/proxy-list',
        'https://2ip.io/proxy/',
        'https://hidemy.life/en/proxy-list-servers',
        'https://freeproxylist.cc'
    ]

    proxy_dict = {}

    print(Fore.YELLOW + "\nFetching Proxies...\n")
    for url in tqdm(urls, desc="Progress", unit=" website"):
        domain, proxies = fetch_proxies(url, print_sample=True)
        proxy_dict[domain] = proxies
        os.system('cls' if os.name == 'nt' else 'clear') 

        print(Fore.YELLOW + Style.BRIGHT + pyfiglet.figlet_format("Proxy Scraper"))
        print(Fore.CYAN + Style.BRIGHT + "Made by: github.com/cr0mb/\n")

    write_proxies_to_file(proxy_dict)
    print(Fore.BLUE + Style.BRIGHT + f"\nAll proxies fetched and saved to proxies.txt.")

if __name__ == "__main__":
    run_proxy_scraper()
