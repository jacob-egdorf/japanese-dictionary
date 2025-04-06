from django.db import models

from mongoengine import *

class JmdictSense(DynamicEmbeddedDocument):
    kanji_restrictions = ListField(StringField())
    pos = ListField(StringField())
    reading_restrictions = ListField(StringField())
    gloss = ListField(DictField())

class JmdictEntry(Document):
    ent_seq = IntField()
    k_ele = ListField(DictField())
    r_ele = ListField(DictField(), required=False)
    sense = EmbeddedDocumentListField(JmdictSense)

    meta = {
        'collection': 'jmdict'
    }
