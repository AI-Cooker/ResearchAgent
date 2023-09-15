import requests
import csv
import time
from bs4 import BeautifulSoup
import sys


def parse_page(url, output):
    # url = "https://mariadb.com/kb/en/troubleshooting-connection-issues/"
    # Headers to mimic a browser visit
    headers = {"User-Agent": "Mozilla/5.0"}

    # Returns a requests.models.Response object
    page = requests.get(
        url, headers=headers, verify="D:\\Storages\\certs\\tma-ADCA-CA.crt"
    )

    soup = BeautifulSoup(page.text, "html.parser")

    with open(output, "w", encoding="utf-8") as file:
        lines = [l for l in soup.get_text().splitlines() if l]
        for line in lines:
            file.write(line + "\n")
