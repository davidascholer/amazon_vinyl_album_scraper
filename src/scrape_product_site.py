import json
import os
import re
import time
from bs4 import BeautifulSoup
import requests
from util import save_image_to_file_system, strip_non_alphanumeric
import html as html_parser

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
    

def scrape_album_from_url(url):

  # Get the data
  response = requests.get(url)
  print("response status: ", response.status_code)
  html = BeautifulSoup(response.text, 'html.parser')
  time.sleep(1.1)
  # html = BeautifulSoup(html_content, 'html.parser')

  # Create the object
  album_object = AlbumObject()

  # Album title
  title_content = html.find(id="productTitle")
  print("title_content", title_content)
  title = title_content.find(text=True).strip()
  album_object.album_title = title
  print("Title: ", title)

  # Artist
  artist_content = html.find(id="bylineInfo")
  artist_inner_content = artist_content.find_all(class_='author')
  artist = artist_inner_content[0].text.strip()
  album_object.artist = artist

  # Create an alphanumeric id
  artist_stripped = strip_non_alphanumeric(artist)
  title_stripped = strip_non_alphanumeric(title)
  album_object.id = f"{artist_stripped}_{title_stripped}"

  # Description
  description_inner_content = html.find(id="productDescription")
  description = description_inner_content.text.strip()
  album_object.description = description

  # Get the image url
  image_content = html.find(id="imgTagWrapperId")
  image_url = image_content.img['src']

  # Details
  details_content = html.find(id="detailBullets_feature_div")
  detail_row = ""
  for count, track in enumerate(details_content.find_all('li')):
          detail_row += f"{track.text.strip()}\n"
  details_json = json.dumps(detail_row)
  album_object.description = re.compile(r"\s+").sub(" ", details_json).strip()

  # Category
  categories_content = html.find(id="wayfinding-breadcrumbs_container")
  categories = []
  for track in categories_content.find_all('li'):
          categories.append(track.text.strip())
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
                