import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from colorama import init, Fore, Style

init(autoreset=True)

def fetch_proxies(url, print_sample=False):
    proxies = []
    try:
        domain = urlparse(url).netloc  
        print(Fore.YELLOW + f"Fetching proxies from {domain}...")  
        response = requests.get(url)
        response.raise_for_status()  
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if 'geonode.com' in url:
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 8:
                    proxy = f"{cols[0].text}:{cols[1].text}"
                    proxies.append(proxy)
        
        elif 'proxyscrape.com' in url:
            proxy_list = response.text.strip().split('\r\n')
            proxies.extend(proxy_list)
        
        elif 'sslproxies.org' in url or 'free-proxy-list.net' in url:
            rows = soup.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    proxy = f"{cols[0].text}:{cols[1].text}"
                    proxies.append(proxy)
        
        elif 'advanced.name' in url:
            proxies_text = soup.get_text()
            proxy_list = proxies_text.split('\n')
            proxies.extend(proxy_list)
        
        elif 'freeproxy.world' in url:
            rows = soup.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    proxy = f"{cols[0].text.strip()}:{cols[1].text.strip()}"
                    proxies.append(proxy)
        
        elif 'echolink.org' in url:
            rows = soup.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 5 and cols[4].text.strip() == 'Ready':
                    proxy = f"{cols[1].text.strip()}:{cols[2].text.strip()}"
                    proxies.append(proxy)

        elif 'iplocation.net' in url:
            rows = soup.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    proxy = f"{cols[0].text.strip()}:{cols[1].text.strip()}"
                    proxies.append(proxy)
        
        print(Fore.GREEN + f"Fetched {len(proxies)} proxies from {domain}.")  
        
        if print_sample and len(proxies) > 5:
            print(Fore.CYAN + "Sample of 5 proxies:")
            for proxy in proxies[:5]:
                print(proxy)
            print()
    
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
    print(Fore.CYAN + Style.BRIGHT + "\n=== Proxy Scraper ===\n")
    print(Fore.YELLOW + Style.BRIGHT + "\nMade by Cr0mb\n")

    urls = [
        'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text',
        'https://www.sslproxies.org/',
        'https://free-proxy-list.net',
        'https://advanced.name/freeproxy/667e4f3871c2f',
        'https://www.freeproxy.world/?country=US',
        'https://www.echolink.org/proxylist.jsp',
        'https://www.iplocation.net/proxy-list',
    ]

    proxy_dict = {}

    for url in urls:
        domain, proxies = fetch_proxies(url, print_sample=True) 
        proxy_dict[domain] = proxies

    write_proxies_to_file(proxy_dict)
    print(Fore.CYAN + f"\nAll proxies fetched and saved to proxies.txt.")

if __name__ == "__main__":
    run_proxy_scraper()