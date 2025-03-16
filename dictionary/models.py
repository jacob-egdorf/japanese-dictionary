from django.db import models

from mongoengine import *

class JmdictSense(EmbeddedDocument):
    kanji_restrictions = ListField(StringField())
    parts_of_speech = ListField(StringField())
    reading_restrictions = ListField(StringField())
    glosses = ListField(StringField())

class JmdictEntry(Document):
    entry_id = IntField()
    kanji = ListField(StringField())
    primary_reading = StringField()
    readings = ListField(StringField())
    senses = EmbeddedDocumentListField(JmdictSense)

    meta = {
        'collection': 'jmdict'
    }
