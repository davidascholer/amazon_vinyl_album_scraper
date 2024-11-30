import pprint
import json
import subprocess
import time

from bs4 import BeautifulSoup
import requests
from scrape_product_site import scrape_album_from_url
from util import object_to_json

# init
if __name__ == '__main__':
  # url = "https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A35%2Cn%3A63942%2Cp_85%3A2470955011&dc&qid=1732963465&rnid=35&ref=sr_pg_1"
  # response = requests.get(url)
  # print(f"response: {response}")
  # html = BeautifulSoup(response.text, 'html.parser')

  # artist_inner_content = html.find_all(class_='title-recipe')
  # for album in html.find_all(class_='title-recipe'):
  #   title_link = album.find_all(class_='a-spacing-mini')[0]
  #   if title_link is None:
  #     continue
  #   link = title_link.a.get('href')
  #   print(f"link: {link}")

  # next_page = html.find_all(class_='s-pagination-next')
  # if next_page is not None and len(next_page) > 0:
  #   next_link = next_page[0].a.get('href')
  #   print(f"next_page: {next_page}")

  # time.sleep(1.1)



  url = 'https://www.amazon.com/Andrews-Sisters-Boogie-Woogie-STEREO/dp/B002QO2X8A/ref=sr_1_3?dib=eyJ2IjoiMSJ9.BNQLirz2s3rODPGmOKGfpFh31ptz1l1A_SxCTq6Y1sPjG-BHAMtBIFiujz8nj7Ao27n4LOt-0BsYg_FhyItaOM7I-1IfrXE88aTmzzI-s-x_HzgPfyVAQ8fm4QfZQjlzasGcMzF8fkDvsV5PPV-m8DmICVDOKQLSjEc64tOBYVpg_KM-ezwzBiQAtUfgptxR72JIwE9B1lpjwRcEbgdjR_DZIz-XQrdqS7p0z9h8qn4.j5a8uiuFF39OGum4WnfBYvl7hdFwcndpiYo_dxxo86k&dib_tag=se&qid=1733008809&rnid=31&s=music&sr=1-3'
  album_object = scrape_album_from_url(url)
  album_json = object_to_json(album_object)
  command = f"echo '{album_json},\n' >> ./output/data.json"
  subprocess.run(command, capture_output=True, shell=True)
  # pprint.pp(f"config_json:\n{album_json}")

# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cp_85%3A2470955011%2Cp_76%3A1249188011&dc&ds=v1%3AQ1At6W79tQeJg0PUivuOFrM%2B%2F%2FBfUoCZmExF%2FhpPiBU&qid=1732960380&rnid=14772275011&ref=sr_nr_n_1&page=2
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cp_85%3A2470955011%2Cp_76%3A1249188011&dc&page=1&qid=1732960392&rnid=14772275011&ref=sr_pg_1
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cp_85%3A2470955011%2Cp_76%3A1249188011&dc&page=3&qid=1732960407&rnid=14772275011&ref=sr_pg_3
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A173425%2Cp_85%3A2470955011%2Cp_76%3A1249188011&dc&page=1&qid=1732960505&rnid=14772275011&ref=sr_pg_1


# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A13463651%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&ds=v1%3AxBJZdsEGky2URPOtMb6x1p7a%2BJPyKwL30Dtrn4hjxtg&qid=1732962247&rnid=31&ref=sr_nr_n_2
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A13463651%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&page=1&ds=v1%3AxBJZdsEGky2URPOtMb6x1p7a%2BJPyKwL30Dtrn4hjxtg&qid=1732962247&rnid=31&ref=sr_pg_1
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A13463651%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&page=2&qid=1732962256&rnid=31&ref=sr_pg_2

# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A5236%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&ds=v1%3AXytmh5341Wzm8NDaAUOVYbxBZ8%2FHzG%2FrsRAXx1MyLOA&qid=1732962247&rnid=31&ref=sr_nr_n_3
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A5236%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&page=2&qid=1732962259&rnid=31&ref=sr_pg_2

# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A470998%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&ds=v1%3AQAm6W4pyQXRW82zt91CgX52PI5hRyVe%2FnPim5snds4E&qid=1732962247&rnid=31&ref=sr_nr_n_4
# https://www.amazon.com/s?i=popular&bbn=14772275011&rh=n%3A5174%2Cn%3A14772275011%2Cn%3A31%2Cn%3A470998%2Cp_85%3A2470955011%2Cp_n_binding_browse-bin%3A387647011&dc&page=2&qid=1732962260&rnid=31&ref=sr_pg_2