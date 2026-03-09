CREATE TABLE card (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    card_passcode_id        INTEGER UNIQUE,
    name                    TEXT,
    type                    TEXT,
    human_readable_card_type TEXT,
    frame_type              TEXT,
    desc                    TEXT,
    race                    TEXT,
    archetype               TEXT,
    attribute               TEXT,
    atk                     INTEGER,
    def                     INTEGER,
    level                   INTEGER,
    scale                   INTEGER,
    linkval                 INTEGER,
    linkmarkers             TEXT,
    typeline                TEXT,
    pend_desc               TEXT,
    monster_desc            TEXT,
    ygoprodeck_url          TEXT,
    image_url               TEXT,
    image_url_small         TEXT,
    image_url_cropped       TEXT,
    price_cardmarket        TEXT,
    price_tcgplayer         TEXT,
    price_ebay              TEXT,
    price_amazon            TEXT,
    price_coolstuffinc      TEXT,
    ban_tcg                 TEXT,
    ban_ocg                 TEXT,
    ban_goat                TEXT
);

CREATE TABLE card_set (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    set_name    TEXT UNIQUE
);

CREATE TABLE card_set_link (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id         INTEGER,
    card_set_id     INTEGER,
    set_code        TEXT,
    set_rarity      TEXT,
    set_rarity_code TEXT,
    set_price       TEXT,
    FOREIGN KEY (card_id) REFERENCES card(id),
    FOREIGN KEY (card_set_id) REFERENCES card_set(id)
);
