# System
import json
import os
import re
# Local
from util import save_image_to_file_system, strip_non_alphanumeric
# Modules
from bs4 import BeautifulSoup
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
        self.amazon_image_url = ""
        self.category = []
        self.disc_tracks = []
        self.language = ""
        self.dimensions = ""
        self.manufacturer = ""
        self.model_number = ""
        self.release_date = ""
        self.availability = ""
        self.label = ""
        self.asin = ""
        self.country_origin = ""
        self.disc_count = ""
        self.discontinued = ""
        self.run_time = ""

    def __str__(self):
        return str(self.__dict__)
    

def scrape_album_from_url(url):

  try:
        print(f"Scraping album from url: {url}")
        # Set up Selenium
        driver = webdriver.Chrome()  # or webdriver.Firefox()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.ID, "imgTagWrapperId")))
        page_source = driver.page_source.encode("utf-8")
        driver.quit()

        # Get the data
        html = BeautifulSoup(page_source, 'html.parser')

        # Create the object
        album_object = AlbumObject()

        # Album title
        title_content = html.find(id="productTitle")
        title = title_content.find(string=True).strip()
        album_object.album_title = json.dumps(title)
        print("Title: ", title)

        # Artist
        artist_content = html.find(id="bylineInfo")
        artist_inner_content = artist_content.find_all(class_='author')
        artist = json.dumps(artist_inner_content[0].text.strip())
        album_object.artist = artist

        # Create an alphanumeric id
        artist_stripped = strip_non_alphanumeric(artist)
        title_stripped = strip_non_alphanumeric(title)
        album_object.id = f"{artist_stripped}_{title_stripped}"

        # Description
        description_inner_content = html.find(id="productDescription")
        description = description_inner_content.text.strip()
        album_object.description = json.dumps(description)

        # Get the image url
        image_content = html.find(id="imgTagWrapperId")
        image_url = image_content.img['src']
        album_object.amazon_image_url = json.dumps(image_url)

        # Details
        details_content = html.find(id="detailBullets_feature_div")
        lists = details_content.find_all('li')
        if lists:
                for detail_row in lists:
                        detail_items = detail_row.find_all(class_='a-list-item')
                        if detail_items[0]:
                                spans = detail_items[0].find_all('span')
                                if len(spans) == 2:
                                        if "Language" in spans[0].text:
                                                album_object.language = spans[1].find(string=True).strip()
                                        if "Product Dimensions" in spans[0].text:
                                                album_object.dimensions = spans[1].find(string=True).strip()
                                        if "Manufacturer" in spans[0].text:
                                                album_object.manufacturer = spans[1].find(string=True).strip()
                                        if "Item model number" in spans[0].text:
                                                album_object.model_number = spans[1].find(string=True).strip()
                                        if "Original Release Date" in spans[0].text:
                                                album_object.release_date = spans[1].find(string=True).strip()
                                        if "Date First Available" in spans[0].text:
                                                album_object.availability = spans[1].find(string=True).strip()
                                        if "Label" in spans[0].text:
                                                album_object.label = spans[1].find(string=True).strip()
                                        if "ASIN" in spans[0].text:
                                                album_object.asin = spans[1].find(string=True).strip()
                                        if "Country of Origin" in spans[0].text:
                                                album_object.country_origin = spans[1].find(string=True).strip()
                                        if "Number of discs" in spans[0].text:
                                                album_object.disc_count = spans[1].find(string=True).strip()
                                        if "Is Discontinued By Manufacturer" in spans[0].text:
                                                album_object.discontinued = spans[1].find(string=True).strip()
                                        if "Run time" in spans[0].text:
                                                album_object.run_time = spans[1].find(string=True).strip()
                        else:
                                print("Error parsing details: detail_items[0] not found")
        else:
              print("Error parsing details: lists not found")

        # Category
        categories_content = html.find(id="wayfinding-breadcrumbs_container")
        categories = []
        for category_item in categories_content.find_all('li'):
                anchors = category_item.find_all('a')
                if anchors:
                        category_item_parsed = json.dumps(anchors[0].text)
                        if category_item_parsed:
                                category_item_parsed = category_item_parsed.strip().replace('\\n', '').replace(' ', '').replace('"',"").replace("'","")
                                print("category_item_parsed",category_item_parsed)
                                categories.append(category_item_parsed)
        album_object.category = categories

        # Download and save the image
        image_ext = os.path.splitext(image_url)[1]
        image_title = f"{artist_stripped}_{title_stripped}_image{image_ext}"
        save_image_to_file_system(image_url, image_title)

        # Iterate through all of the tracks on all of the discs
        track_listing = html.find(id="musicTracks_feature_div")
        disc_count = 1
        for disc in track_listing.find_all(class_='a-row'):
                disc_track_list = []
                track_count = 1
                for count, track in enumerate(disc.find_all('td')):
                        if count % 2 == 1:
                                track_listings_dict = {f"Track {track_count}":track.text.strip()}
                                track_count += 1
                                disc_track_list.append(track_listings_dict)
                disc_object = {f"Disc {disc_count}": disc_track_list}
                album_object.disc_tracks.append(disc_object)
                disc_count += 1
        return album_object
  
  except Exception as e:
        print(f"Error scraping album: {e}")
        return None
                
# if __name__ == '__main__':
#         scrape_album_from_url("https://www.amazon.com/Walking-Proof-LILLY-HIATT/dp/B083LQQD6N/ref=sr_1_17?dib=eyJ2IjoiMSJ9.ZkV9YHtx7twT9jz4qZ2ZJEO3CgMQiezzhQSPShL3rjLMCvpWAfnTkf7p96Vuy9hW5tCRbQGScI2-Gn_8R16NDVp93mB9hNaRUfeFesPOlPFc7KLOOz34_3Lrs5dj6JfGdLYNjCL03wcn851JnxcDkoflGQzcvy0tfw1XQ7wPQmB5hC69j7UPtt_mde4Y2pHpifHT70vPxQUD_lCm-xyoqANH3EUCHk1rXY7pB2HJNzo.D4I-CQEXsa4j6rcWA--XA-D06R4ncw_87rHJwgYJnso&dib_tag=se&qid=1733015736&refinements=p_85%3A2470955011&rnid=35&rps=1&s=music&sr=1-17")