from database.db import db

class authoritative_zone(db.Document):
    zone_name=db.StringField(required=True, unique=True)
    primary_server=db.StringField(required=True, unique=True)
    EA=db.ListField( required=False)
    Records=db.ListField(required=False,unique=True)
    #Arecord=db.ListField(required=False,unique=True)
