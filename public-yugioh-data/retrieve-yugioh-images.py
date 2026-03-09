import urllib.request
import urllib.error
import json
import os
import time

top10_only = True
card_delay_seconds = 1
this_dir = os.path.dirname(os.path.abspath(__file__))
yugioh_json_file_path = os.path.join(this_dir, "public-yugioh-card-data.json")

print("Read Yu-Gi-Oh data")
with open(yugioh_json_file_path, "r") as f:
    yugioh_data_json = json.load(f)

cards = yugioh_data_json["data"]

if top10_only:
    cards = cards[:10]

os.makedirs(os.path.join(this_dir, "images", "cards"), exist_ok=True)
os.makedirs(os.path.join(this_dir, "images", "cards_small"), exist_ok=True)
os.makedirs(os.path.join(this_dir, "images", "cards_cropped"), exist_ok=True)

print("Download Yu-Gi-Oh images")
for card in cards:
    card_id = card["id"]
    card_image = next(img for img in card["card_images"] if img["id"] == card_id)

    yugioh_image_url = card_image["image_url"]
    yugioh_image_file_path = os.path.join(this_dir, "images", "cards", os.path.basename(yugioh_image_url))
    try:
        yugioh_image_data = urllib.request.urlopen(yugioh_image_url).read()
        with open(yugioh_image_file_path, "wb") as f:
            f.write(yugioh_image_data)
        print("Save", yugioh_image_file_path)
    except urllib.error.HTTPError:
        print("Not found", yugioh_image_file_path)

    yugioh_image_url = card_image["image_url_small"]
    yugioh_image_file_path = os.path.join(this_dir, "images", "cards_small", os.path.basename(yugioh_image_url))
    try:
        yugioh_image_data = urllib.request.urlopen(yugioh_image_url).read()
        with open(yugioh_image_file_path, "wb") as f:
            f.write(yugioh_image_data)
        print("Save", yugioh_image_file_path)
    except urllib.error.HTTPError:
        print("Not found", yugioh_image_file_path)

    yugioh_image_url = card_image["image_url_cropped"]
    yugioh_image_file_path = os.path.join(this_dir, "images", "cards_cropped", os.path.basename(yugioh_image_url))
    try:
        yugioh_image_data = urllib.request.urlopen(yugioh_image_url).read()
        with open(yugioh_image_file_path, "wb") as f:
            f.write(yugioh_image_data)
        print("Save", yugioh_image_file_path)
    except urllib.error.HTTPError:
        print("Not found", yugioh_image_file_path)

    time.sleep(card_delay_seconds)

print("Finished download and save")
