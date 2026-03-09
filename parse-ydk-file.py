import os

def process_ydk_data(ydk_data):
    main = []
    extra = []
    side = []

    lines = ydk_data.split("\n")
    section = None

    for line in lines:
        line = line.strip()

        if "#main" in line:
            section = "main"
        elif "#extra" in line:
            section = "extra"
        elif "!side" in line:
            section = "side"
        elif line != "" and section == "main":
            card_id = int(line)
            main.append(card_id)
        elif line != "" and section == "extra":
            card_id = int(line)
            extra.append(card_id)
        elif line != "" and section == "side":
            card_id = int(line)
            side.append(card_id)

    return {"main": main, "extra": extra, "side": side}


this_dir = os.path.dirname(os.path.abspath(__file__))
ydk_file_path = os.path.join(this_dir, "sample-ydk-files", "Mitsurugi.ydk")

ydk_file = open(ydk_file_path, "r")
ydk_data = ydk_file.read()
ydk_file.close()

deck = process_ydk_data(ydk_data)

print("Main:", deck["main"])
print("Extra:", deck["extra"])
print("Side:", deck["side"])
