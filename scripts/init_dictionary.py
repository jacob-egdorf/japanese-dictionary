import logging
import os
import xml.etree.ElementTree
import xml.dom

from pymongo import MongoClient

if __name__ == "__main__":
    database = os.environ.get("MONGODB_DATABASE")
    jmdict_path = os.environ.get("JMDICT_PATH")
    debug = os.environ.get("DEBUG")
    log_level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=log_level,
        handlers=[logging.StreamHandler()]
    )

    client = MongoClient(f"mongodb://db:27017/{database}")
    db = client[database]
    collection = db.jmdict
    collection.drop()
    collection.create_index(
        [("kanji", "text"), ("readings", "text"), ("senses.glosses", "text")]
    )

    element_tree = xml.etree.ElementTree.parse(jmdict_path)
    root = element_tree.getroot()

    for entry in root.findall("entry"):
        entry_document = {
            "entry_id": "",
            "primary_reading": "",
            "readings": [],
            "kanji": [],
            "senses": [],
        }

        entry_document["entry_id"] = int(entry.find("ent_seq").text)

        reading_elements = entry.findall("r_ele")
        if reading_elements:
            for elem in reading_elements:
                entry_document["readings"].append(elem.find("reb").text)

        kanji_elements = entry.findall("k_ele")
        if kanji_elements:
            for elem in kanji_elements:
                entry_document["kanji"].append(elem.find("keb").text)

        if entry_document["kanji"]:
            entry_document["primary_reading"] = entry_document["kanji"][0]
        elif entry_document["readings"]:
            entry_document["primary_reading"] = entry_document["readings"][0]

        senses = entry.findall("sense")
        for sense in senses:
            sense_data = {
                "parts_of_speech": [],
                "reading_restrictions": [],
                "kanji_restrictions": [],
                "glosses": [],
            }

            poses = sense.findall("pos")
            for pos in poses:
                sense_data["parts_of_speech"].append(pos.text)

            stagrs = sense.findall("stagr")
            if stagrs:
                for stagr in stagrs:
                    sense_data["reading_restrictions"].append(stagr.text)

            stagks = sense.findall("stagk")
            if stagks:
                for stagk in stagks:
                    sense_data["kanji_restrictions"].append(stagk.text)

            glosses = sense.findall("gloss")
            for gloss in glosses:
                sense_data["glosses"].append(gloss.text)

            entry_document["senses"].append(sense_data)

        logging.debug(f"Inserting entry for {entry_document['primary_reading']}: {entry_document}")
        collection.insert_one(entry_document)
