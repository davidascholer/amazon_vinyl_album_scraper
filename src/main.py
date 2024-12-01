import subprocess
from scrape_product_site import scrape_album_from_url
from scrape_links import get_links_from_page
from util import object_to_json
import shlex

def save_album_to_file_system(url):

  # Get all of the listings from each page
  links = get_links_from_page(url)
  # print(f"next: {links["next"]}")

  # Scrape each page and save the object and image to the file system
  try:
    for album_link in links["album_links"]:
      print(f"calling scrape_album_from_url")
      album_object = scrape_album_from_url(album_link)
      if album_object is None:
        continue
      print("calling object_to_json")
      album_json = object_to_json(album_object)
      print("saving to data.json")
      try:
        with open("./output/data.json", "a") as file:
          file.write(f"{album_json}\n")
      except Exception as e:
        print(f"Error saving album: {e}")

  except Exception as e:
    print(f"Error saving album: {e}")

  if(links["next"] is not None):
    next_page = links["next"]
    print("next page: ", next_page)
    save_album_to_file_system(next_page)

# init
if __name__ == '__main__':
  url = "https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cp_85%3A2470955011&dc&page=68&qid=1733035433&rnid=14772275011&ref=sr_pg_68"
  save_album_to_file_system(url)
  command = f"echo '\n' >> ./output/data.json"
  subprocess.run(command, capture_output=True, shell=True)
