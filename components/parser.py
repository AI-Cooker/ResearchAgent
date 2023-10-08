import requests
import csv
import time
from bs4 import BeautifulSoup
import sys
import re


def parse_page(url, output):
    # url = "https://mariadb.com/kb/en/troubleshooting-connection-issues/"
    # Headers to mimic a browser visit
    headers = {"User-Agent": "Mozilla/5.0"}

    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(page.text, "html.parser")

    with open(output, "w", encoding="utf-8") as file:
        striped_text = re.sub(r"\n\s*\n", "\n", soup.get_text(), flags=re.MULTILINE)
        lines = [l for l in striped_text.splitlines() if l]
        for line in lines:
            file.write(line + "\n")
