import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import threading


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]

def fetch_with_playwright(url):
    """Fetch the rendered HTML text (up to 2000 chars) from a page using Playwright in a thread."""
    result = {}

    def run():
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)  # allow 60s for slower JS sites
            content = page.content()
            title = page.title()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        for irrelevant in soup(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.get_text(separator="\n", strip=True)
        result["data"] = (title + "\n\n" + text)[:2000]

    thread = threading.Thread(target=run)
    thread.start()
    thread.join()

    return result.get("data", "Error: No content fetched")