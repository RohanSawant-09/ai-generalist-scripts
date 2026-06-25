import requests
from bs4 import BeautifulSoup

def fetch_webpage(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code !=200:
        print(f"Failed to fetch page. Status code:{response.status_code}")
        return None

    return response.text

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
        tag.decompose()

    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines()]
    clean_lines = [line for line in lines if line]

    return '\n'.join(clean_lines)

def save_text(text, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved text to {filepath}")

# Run it
url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
html = fetch_webpage(url)

if html:
    text = extract_text(html)
    save_text(text, 'ai-wikipedia.txt')
    print(f"Extracted {len(text.split())} words")
    print("\nFirst 500 characters:")
    print(text[:500])