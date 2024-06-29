
# Proxy-Scraper
[Video Tutorial](https://youtu.be/gR-AhoWpbaI)


Proxy Scraper is a Python script designed to fetch and save proxies from multiple sources to a file. It supports fetching proxies from various websites using BeautifulSoup and requests libraries.

<img src="https://github.com/Cr0mb/Proxy-Scraper/assets/137664526/70f997b8-d26b-4b1d-a3ba-4ba881a4480a" alt="image" width="300" />


# How it works

When you run Proxy Scraper, it accesses each specified URL containing a list of proxies. It then parses the HTML content of these pages using BeautifulSoup, extracting relevant proxy information such as IP address and port number. The script handles different HTML structures from each website to ensure compatibility and accurate extraction.

## Features

- Fetches proxies from:

  - [Proxyscrape.com](proxyscrape.com)
  - [sslproxies.org](sslproxies.org)
  - [free-proxy-list.net](free-proxy-list.net)
  - [advanced.name](advanced.name)
  - [freeproxy.world](freeproxy.world)
  - [echolink.org](echolink.org)
  - [iplocation.net](iplocation.net)

- Saves fetched proxies to proxies.txt.

- Displays a sample of 5 fetched proxies from each source.

## Requirements
- Python 3.x
- Install Dependencies
```
pip install requests beautifulsoup4 colorama
```

## Run Script
```
python proxy_scraper.py
```
<h2 align="center"> *Disclaimer* </h2>

<h2 align="center">This script is intended for educational and testing purposes only. Use it responsibly and do not use the proxies obtained for any illegal activities. The creator of this script is not responsible for any misuse or damage caused by the misuse of the fetched proxies.</h2>
