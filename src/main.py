import pprint
import json
from scrape_product_site import create_album

def object_to_json(config_object):
    return json.dumps(config_object.__dict__)

# init
if __name__ == '__main__':
  album_object = create_album()
  config_json = object_to_json(album_object)
  pprint.pp(f"config_json:\n{config_json}")

