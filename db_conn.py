from flask import Flask
from flask import request
from flask import jsonify,Response
from database.db import intialize_db as db
from database.models import authoritative_zone
import json
from flask import render_template
from flask import  jsonify
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["DNS"]
mycol = mydb["authoritative_zone"]


def update_tags(name, data):
    data={"$push":data}
    print(data)
    name=({"zone_name":name})
    work=mycol.update_one(name,data)
    return (str(work.raw_result))

def delete_tags(query):
    #{"name": "arec_inf2.test100.com","ip_address": "10.35.101.11"}
    print("query",query)
    result=mycol.update({"Records":[{"a":[query]}]},{"$set":{"Records":[{"a":[]}]}})
    #result=mycol.delete_one(query)
    return (str(result))

#zone={"zone_name": "test100.com"}
#data=({"$push": {'Records': [{'a': [{'name': 'arec99.test100.com', 'ip_address': '11.11.21.29'}]}]}})
#articles=update_tags(zone,data)
#print (articles)
#mycol.update_one({"zone_name": "test100.com"}, {"$push": {'Records': [{'a': [{'name': 'arec509.test100.com', 'ip_address': '11.11.11.29'}]}]}})

#{'Records': [{'a': [{'name': 'arec177.test100.com', 'ip_address': '11.11.11.25'}]}]}