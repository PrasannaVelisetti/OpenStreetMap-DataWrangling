"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json
import codecs

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
Postcodes_Expected=re.compile(r'^\d{6}$')

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')  #Establishing connection to MongoDb
    db = client[db_name]
    return db

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        address={}
        created_dict={}
        lat_value=(element.get("lat"))
        lon_value=(element.get("lon"))
        
        for e in element.attrib.keys():
            if e in CREATED:
                created_dict[e]=element.get(e)
            if (e not in ["lat","lon"]) & (e not in CREATED) :
                node[e]=element.get(e)
        if (element.get("lat") and element.get("lon")):
            node["pos"]=[float(element.get("lat")), float(element.get("lon"))] #Creating pos key for the latitude and longitude pair
        if element.tag=="node":                                                #Creating type key to denote whethere the document is node or way
            node["type"]="node"
        else:
            node["type"]="way"
        node["created"]=created_dict
        
        
        for tag in element.iter("tag"):
            tag_kvalue=tag.get("k")
            if not (tag_kvalue.split(':', 1)[0]=="addr"):
                node[tag.get("k")]=tag.get("v")
            if (tag_kvalue.split(':', 1)[0]=="addr" and tag_kvalue.rsplit(':', 1)[0]=="addr"):
                if (tag_kvalue.split(':', 1)[1]=="postcode"):           #Cleaning postcodes
                    if bool(Postcodes_Expected.search((tag.get("v")))):
                        address[tag_kvalue.split(':', 1)[1]]=(tag.get("v"))[:2]
                    if (tag.get("v")=="Singapore 408564"):
                        address[tag_kvalue.split(':', 1)[1]]="40"
                    if (tag.get("v")=="437 437"):
                        address[tag_kvalue.split(':', 1)[1]]="43"    
                else:
                    address[tag_kvalue.split(':', 1)[1]]=tag.get("v")
        
        if address:
            node["address"]=address
           
        node_ref=[]
        if element.tag=="way":
            for nd in element.iter("nd"):
                node_ref.append(nd.get("ref"))
            node["node_refs"]=node_ref
                   
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
   
    data = process_map('Singapore.osm', False)
   # pprint.pprint(data)
    

if __name__ == '__main__':
    test()