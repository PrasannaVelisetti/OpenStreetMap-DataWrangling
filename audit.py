#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

postalcode=re.compile(r'^\d{6}$')
phonenumber=re.compile("([+]\d{2}[-\s]\d{4}\d{4})|([+]\d{2}\d{4}\d{4})|([+]\d{2}[-\s]\d{4}[\s]\d{4})|(\d{4}\d{4})|(\d{4}[-\s]\d{4})|([+]\d{2}[-\s]\d{2}[-\s]\d{3}[-\s]\d{3})|([+]\d{2}[-\s]\d{5}[-\s]\d{3})|([+]\d{2}[-\s]\d{4}[-\s]\d{3}[-\s]\d{4})|(\d{4}[-\s]\d{3}[-\s]\d{4})")



def key_type(element, keys):
    name="NoName"
    for tag in element.iter("tag"):
        tag_kvalue=tag.get("k")
        if(tag_kvalue=="name"):
            name=tag.get("v")
    for tag in element.iter("tag"):
        flag=0
        tag_kvalue=tag.get("k")
        if (tag_kvalue.split(':', 1)[0]=="addr" and tag_kvalue.rsplit(':', 1)[0]=="addr"):
            if (tag_kvalue.split(':', 1)[1]=="postcode"):
                if not bool(postalcode.search((tag.get("v")))):
                    print (tag.get("v"))
                    print name
                    keys["WrongPostcode"]+=1
        if (tag_kvalue=="phone"):
            if not bool(phonenumber.search((tag.get("v")))):
                print (tag.get("v"))
                keys["WrongPhone"]+=1
    return keys



def process_map(filename):
    keys = {"WrongPostcode": 0,"WrongPhone": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
  
    keys = process_map('Singapore.osm')
    pprint.pprint(keys)
   


if __name__ == "__main__":
    test()