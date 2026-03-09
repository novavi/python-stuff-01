import json
import os
import sqlite3

top10_only = True

this_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(this_dir, "public-yugioh-card-data.json")
database_file_path = os.path.join(this_dir, "yugioh.db")

print("Read Yu-Gi-Oh data")
json_file = open(json_file_path, "r")
yugioh_data_json = json.load(json_file)
json_file.close()
cards = yugioh_data_json["data"]

if top10_only:
    cards = cards[:10]

database = sqlite3.connect(database_file_path)

for card in cards:

    print("Load card", card["id"], card["name"])
    card_id = card["id"]
    card_name = card["name"]
    card_type = card["type"]
    human_readable_card_type = card["humanReadableCardType"]
    frame_type = card["frameType"]
    card_desc = card["desc"]
    race = card["race"]
    archetype = card.get("archetype")
    attribute = card.get("attribute")
    atk = card.get("atk")
    def_ = card.get("def")
    level = card.get("level")
    scale = card.get("scale")
    linkval = card.get("linkval")
    ygoprodeck_url = card["ygoprodeck_url"]

    linkmarkers = None
    if "linkmarkers" in card:
        linkmarkers = ",".join(card["linkmarkers"])

    typeline = None
    if "typeline" in card:
        typeline = ",".join(card["typeline"])

    pend_desc = card.get("pend_desc")
    monster_desc = card.get("monster_desc")

    card_image = None
    for img in card["card_images"]:
        if img["id"] == card_id:
            card_image = img
            break

    image_url = card_image["image_url"]
    image_url_small = card_image["image_url_small"]
    image_url_cropped = card_image["image_url_cropped"]

    card_prices = card["card_prices"][0]
    price_cardmarket = card_prices["cardmarket_price"]
    price_tcgplayer = card_prices["tcgplayer_price"]
    price_ebay = card_prices["ebay_price"]
    price_amazon = card_prices["amazon_price"]
    price_coolstuffinc = card_prices["coolstuffinc_price"]

    ban_tcg = None
    ban_ocg = None
    ban_goat = None
    if "banlist_info" in card:
        ban_tcg = card["banlist_info"].get("ban_tcg")
        ban_ocg = card["banlist_info"].get("ban_ocg")
        ban_goat = card["banlist_info"].get("ban_goat")

    database.execute("""
        INSERT OR IGNORE INTO card (
            card_id, name, type, human_readable_card_type, frame_type,
            desc, race, archetype, attribute, atk, def, level, scale,
            linkval, linkmarkers, typeline, pend_desc, monster_desc,
            ygoprodeck_url, image_url, image_url_small, image_url_cropped,
            price_cardmarket, price_tcgplayer, price_ebay, price_amazon, price_coolstuffinc,
            ban_tcg, ban_ocg, ban_goat
        ) VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?
        )
    """, (
        card_id, card_name, card_type, human_readable_card_type, frame_type,
        card_desc, race, archetype, attribute, atk, def_, level, scale,
        linkval, linkmarkers, typeline, pend_desc, monster_desc,
        ygoprodeck_url, image_url, image_url_small, image_url_cropped,
        price_cardmarket, price_tcgplayer, price_ebay, price_amazon, price_coolstuffinc,
        ban_tcg, ban_ocg, ban_goat
    ))

    inserted_card = database.execute("""
        SELECT id FROM card
        WHERE card_id = ?
    """, (card_id,)).fetchone()
    card_record_id = inserted_card[0]

    for card_set in card.get("card_sets", []):
        set_name = card_set["set_name"]
        set_code = card_set["set_code"]
        set_rarity = card_set["set_rarity"]
        set_rarity_code = card_set["set_rarity_code"]
        set_price = card_set["set_price"]

        database.execute("""
            INSERT OR IGNORE INTO card_set (set_name)
            VALUES (?)
        """, (set_name,))
        inserted_card_set = database.execute("""
            SELECT id FROM card_set
            WHERE set_name = ?
        """, (set_name,)).fetchone()
        card_set_record_id = inserted_card_set[0]

        database.execute("""
            INSERT OR IGNORE INTO card_set_link (card_id, card_set_id, set_code, set_rarity, set_rarity_code, set_price)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (card_record_id, card_set_record_id, set_code, set_rarity, set_rarity_code, set_price))

database.commit()
database.close()
print("Finished load")
