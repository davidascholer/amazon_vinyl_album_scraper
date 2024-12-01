import json
import os
import re
from bs4 import BeautifulSoup
from util import save_image_to_file_system, strip_non_alphanumeric
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AlbumObject(object):

    def __init__(self):
        self.id = ""
        self.album_title = ""
        self.artist = ""
        self.description = ""
        self.category = []
        self.disc_tracks = []

    def __str__(self):
        return str(self.__dict__)
    

def get_links_from_page(url):
    
    base_url = "https://www.amazon.com"
    
    # Set up Selenium
    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'a-spacing-mini')))
    page_source = driver.page_source.encode("utf-8")
    driver.quit()

    html = BeautifulSoup(page_source, 'html.parser')

    listings = html.find_all(class_='s-title-instructions-style')
    print("listing count: ", len(listings))
    album_links = []
    for listing in listings:
        # Link is an ad. Skip it.
        sponsored_links = listing.find_all(class_='a-spacing-micro')
        if sponsored_links is not None and len(sponsored_links) > 0:
            #  print("sponsor link")
             continue
        # Link is an album. Append it.
        albums = listing.find_all(class_='a-size-mini')
        for album in albums:
            # print(f"album link")
            link = base_url+album.a.get('href')
            # print(f"link: {link}")
            album_links.append(link)

    next_link = None
    next_page = html.find_all(class_='s-pagination-next')
    if next_page is not None and len(next_page) > 0:
        if next_page[0].get('href') is not None:
            next_link = base_url+next_page[0].get('href')
            
    return {"album_links": album_links, "next": next_link}
                