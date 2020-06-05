from flask import Flask
from flask import request
from flask import jsonify,Response
from database.db import intialize_db as db
from database.models import authoritative_zone
import json
from flask import render_template
from zones.db_conn import update_tags as ut
from zones.db_conn import delete_tags as dt

app = Flask(__name__)
app.config['MONGODB_SETTINGS']={
    'host':'mongodb://localhost/DNS'
}
db=db(app)

def exclude_keys(dic,excluding):
    return {x: dic[x] for x in dic if x not in excluding}

@app.route("/")
def home():
    return "Infoblox Home Page!"


@app.route("/zone_auth",methods=["POST"])
def zone_auth():
    data=request.get_json()
    result=authoritative_zone(**data).save()
    id=result.id
    return {'id':str(id)},200


#add check here
@app.route("/zone_auth",methods=["GET"])
def get_zone_auth():
    result=[]
    get_zone_details= (authoritative_zone.objects()).to_json()
    get_zone_details=json.loads(get_zone_details)
    for details in get_zone_details:
        excluding = ['EA', 'Records']
        get_data=exclude_keys(details, excluding)
        result.append(get_data)
    return (str(result))


@app.route("/zone_auth/<id>",methods=["PUT"])
def update_zone_auth(id):
    update_zone_details=request.get_json()
    print (update_zone_details)
    if 'zone_name' in update_zone_details.keys() :
        return ("Zone_name cannot be updated ")
    else:
        authoritative_zone.objects.get(id=id).update(upsert=True,**update_zone_details)
        return Response("Primary server updated for requested zone",status=200)


@app.route("/zone_auth/<id>",methods=["DELETE"])
def delete_zone_auth(id):
    authoritative_zone.objects.get(id=id).delete()
    return Response("Zone deleted ",status=200)


@app.route("/zone_auth/<id>/record:a",methods=["POST"])
def add_a_record(id):
    result=""
    data=request.get_json()
    get_zone_details= (authoritative_zone.objects()).to_json()
    get_zone_details=json.loads(get_zone_details)
    print ("get_zone_details:",get_zone_details)
    print("TYPE get_zone_details:", type(get_zone_details))
    dict1={}
    #print ("Record details :",get_zone_details['Records'])
    record_name=""
    for i in data.items():
        for j in i[1][0].values():
            for k in j:
                #print (k['name'])
                record_name=str(k['name'])
                print (record_name)
    zone_name=record_name.partition('.')
    print ("zone name : ",zone_name)
    print ("details zone_name:",[details['zone_name'] for details in get_zone_details])
    #print ("get zone details 0 : ",get_zone_details[0]['Records'])   ### try here

    record_check=data["Records"][0]['a'][0]['name']
    ipaddress_check = data["Records"][0]['a'][0]['ip_address']

### A Record get from database #####

    #print ("details zone_name:", [details['zone_name'] for details in get_zone_details])
    get_zone_details = (authoritative_zone.objects()).to_json()
    get_zone_details = json.loads(get_zone_details)
    for details in get_zone_details:
        excluding = ['EA', 'primary_server']
        record = exclude_keys(details, excluding)
        print("Check here !!!!!!!!!!!!!", type(record))

        if (record['Records'] != []):
            for i in record['Records']:
                for j in i:
                    print(j['a'][0]['ip_address'])
                    print ("record check : ",record_check)
                    print ("ip address :",ipaddress_check)
                    print ("main name:",j['a'][0]['name'])
                    print ("main ip:",j['a'][0]['ip_address'])
                    if ((record_check != j['a'][0]['name']) and (ipaddress_check != j['a'][0]['ip_address'])):
                        if (zone_name[-1] in [details['zone_name'] for details in get_zone_details]):
                            for details in get_zone_details:
                                print ("details:", details)
                                if (details['zone_name'] == zone_name[-1]):
                                    print ("zone_name", zone_name)
                                    print ("Records :", dict(data))
                                    result = ut(zone_name[-1], data)
                                    print (result)
                                else:
                                    print ("Please create a zone to add records ")
                    return (jsonify("Record already exsists"))
        else:
            if (zone_name[-1] in [details['zone_name'] for details in get_zone_details]):
                for details in get_zone_details:
                    print ("details:", details)
                    if (details['zone_name'] == zone_name[-1]):
                        print ("zone_name", zone_name)
                        print ("Records :", dict(data))
                        result = ut(zone_name[-1], data)
                        print (result)
                    else:
                        return ("Please create a zone to add records ")
    return (result)
    print("record is added !!!!!")
                    #else:
                    #    print ("Record name or ip_address already exists !!!!!!!!")


@app.route("/zone_auth/record:a",methods=["GET"])
def get_a_record():
    result = []
    get_zone_details = (authoritative_zone.objects()).to_json()
    get_zone_details = json.loads(get_zone_details)
    for details in get_zone_details:
        excluding = ['EA', 'primary_server']
        get_data = exclude_keys(details, excluding)
        print("Check here !!!!!!!!!!!!!",get_data)
        result.append(get_data)
    return (jsonify(result))


@app.route("/zone_auth/<id>/record:a",methods=["PUT"])
def update_a_record(id):
    update_record_details = request.get_json()
    print(update_record_details)
    if 'name' in update_record_details.keys():
        return ("Record Name cannot be updated ")
    else:
        authoritative_zone.objects.get(id=id).update(upsert=True,**update_record_details)
        return Response("Requested IP address updated for requested Record", status=200)

@app.route("/zone_auth/<id>/record:a",methods=["DELETE"])
def delete_a_record(id):
    data=request.get_json()
    print (data)
    result=dt(data)
    return Response(result)

if __name__ == "__main__":
    app.run(debug=True)