import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import date,timedelta
import os
from pathlib import Path


logger = logging.getLogger(__name__)
logging.basicConfig(filename='scrapping.log',level=logging.INFO)

def find_urls(key_url):
    '''
    Uses requests and BeautifulSoup to extract weather-related article URLs.

    Args:
        key_url (str): The main URL that contains the target article links.

    Returns:
        list of str: A list of extracted URLs.
    '''
    response = requests.get(key_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    all_text = soup.find_all(class_="read-title")
    links = list()
    for i in all_text:
        links.append(i.find("a")["href"])
    if links:
        links_cleaned = list()
        for i in links:
            if "previsao-do-tempo" in i:
                links_cleaned.append(i)
            else:
                pass
    return links_cleaned

def writing(new_urls):
    '''
    Writes the new URLs to a .txt file named with the current date.

    Args:
        new_urls (iterable): A list or set of URLs to be saved.

    Logs:
        - If writing fails, logs an error message.
    '''
    actual_date = date.today()
    path = Path(__file__).resolve().parent.parent.parent
    diretorios = [item.name for item in path.iterdir() if item.is_dir()]
    if "webscrappingfiles" not in diretorios:
        os.mkdir(f"{path}/webscrappingfiles")
        os.mkdir(f"{path}/webscrappingfiles/urls")
    if new_urls is None:
        logger.info(f"No URLs Today {actual_date}")
    try:
        with open(f"{path}/webscrappingfiles/urls/{actual_date}.txt","w") as f:
            for url in new_urls:
                f.write("%s\n"%url)
    except:
     logger.info("An unexpected error occured writing the URLS")

def opening_oldurls(past_date):
    '''
    Opens a .txt file containing previously stored URLs.

    Args:
        past_date (datetime.date): The date (in ISO format) of the file to be opened.

    Returns:
        set of str: A set of previously stored URLs.
    '''
    path = Path(__file__).resolve().parent.parent.parent
    with open(f"{path}/webscrappingfiles/urls/{past_date}.txt") as f:
        old_urls = f.read().split("\n")
        old_urls = set(old_urls)
    return old_urls


def compare_urls(new_urls):
    '''
    Compares new URLs with those saved from previous days and returns only the unseen ones.

    Args:
        new_urls (list of str): List of recently obtained URLs.

    Returns:
        set of str: A set of URLs not found in the recent history.
    '''
    actual_date = date.today()
    past_date = actual_date - timedelta(days=1)
    try:
        old_urls = opening_oldurls(past_date)
        return set(new_urls) - old_urls
    except FileNotFoundError:
        for days in range(1,10):
            past_date = actual_date - timedelta(days=days)
            try:
                print(past_date)
                old_urls = opening_oldurls(past_date=past_date)
                if old_urls:
                    return set(new_urls) - old_urls
            except:
                pass
    return None

def return_info(info_url):
    """
    For each URL, makes an HTTP GET request, parses the HTML with BeautifulSoup,
    and extracts the 3rd paragraph's text (index 2), splitting at line breaks
    and returning the first line of that paragraph.

    Args:
        info_url (list of str): List of URLs to fetch content from.

    Returns:
        list of str: A list of extracted text snippets from the 3rd paragraph of each page.

    Logs:
        - If a request fails, logs the URL.
    """
    informations = list()
    for i in info_url:
        try:
            response = requests.get(i)
            response.encoding = 'utf-8'
        except:
            logger.info(f"Error with Connection on the URL:{i}.")
            continue
        soup = BeautifulSoup(response.text,'html.parser')
        x = soup.find_all("p")
        for i,data in enumerate(x):
            if i == 2:
                text_target = data.get_text()
            else:
                pass
        informations.append(text_target.split("\n")[0])
        time.sleep(2)
    return informations

