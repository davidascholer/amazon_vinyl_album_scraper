import requests
import re

def save_image_to_file_system(image_url, image_title):
        try:
                img_data = requests.get(image_url).content
                with open(f'../images/{image_title}', 'wb') as handler:
                        handler.write(img_data)
        except Exception as e:
                print(f"Error saving image: {e}")

def strip_non_alphanumeric(text):
        return re.sub(r'[^A-Za-z0-9]', '', text)
