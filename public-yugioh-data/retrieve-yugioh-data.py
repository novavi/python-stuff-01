import urllib.request
import json
import os

print("Download public Yu-Gi-Oh data")
# ygoprodeck_api_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?id=6983839"
ygoprodeck_api_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
# yugioh_headers = {"User-Agent": "Mozilla/5.0"}
yugioh_headers = {"User-Agent": "Skyler_Novavi_NEA_Project/1.0"}
yugioh_request = urllib.request.Request(ygoprodeck_api_url, headers=yugioh_headers)
yugioh_response = urllib.request.urlopen(yugioh_request)
yugioh_data_str = yugioh_response.read().decode()
yugioh_data_json = json.loads(yugioh_data_str)

this_dir = os.path.dirname(os.path.abspath(__file__))
yugioh_file_path = os.path.join(this_dir, "public-yugioh-card-data.json")

print("Save public Yu-Gi-Oh data")
with open(yugioh_file_path, "w") as f:
    json.dump(yugioh_data_json, f, indent=2)

print("Finished download and save")
