import logging
import os

import xmltodict
from pymongo import MongoClient

def postprocessor(path, key, value):
    if key == "ent_seq":
        return key, int(value)
    return key.replace("#", ""), value

if __name__ == "__main__":
    database = os.environ.get("MONGODB_DATABASE")
    jmdict_path = os.environ.get("JMDICT_PATH")
    debug = os.environ.get("DEBUG")
    log_level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=log_level,
        handlers=[logging.StreamHandler()]
    )

    with open(jmdict_path, "r", encoding="utf-8") as xml_file:
        jmdict = xmltodict.parse(
            xml_file.read(), disable_entities=False, 
            force_list={'k_ele', 'r_ele', 'sense', 'gloss', 'stagk', 'stagr', 'pos', 'misc', 'ke_pri', 're_pri'},
            postprocessor=postprocessor
        )

    client = MongoClient(f"mongodb://db:27017/{database}")
    db = client[database]
    collection = db.jmdict
    collection.drop()
    collection.create_index(
        [("k_ele.keb", "text"), ("r_ele.reb", "text"), ("sense.gloss.text", "text")]
    )

    collection.insert_many(jmdict["JMdict"]["entry"])
