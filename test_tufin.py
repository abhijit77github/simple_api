# test file




#1. get all devices from https://tufin-dev.nml.com/securetrack/api/devices/
import requests as rq
import json
import requests
import xml.etree.ElementTree as ET
import xmltodict
from pprint import pprint
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# #print(myroot)
# print(myroot.tag)

DEVICE_ID_ENDPOINT = "https://tufin-dev.nml.com/securetrack/api/devices"
DEVICE_RULE_ENDPOINT = "https://tufin-dev.nml.com/securetrack/api/devices/{}/rules"
UTAN_NO_ENDPOINT = "https://tufin-dev.nml.com/securetrack/api/devices/{}/rules/{}"

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Qk1PMzUwMjpSZXlvbmFjaGhvcmlAMjAyMQ==',
    'Cookie': 'JSESSIONID=D2DBCFAA0A4135FAC61062ADA4023572'
    }

def make_request(request_type="GET", endpoint=None, data={}, headers=None):

    if request_type == "GET":
    # print(f"get request : {request_type}")
        resp = rq.request("GET", endpoint, headers=HEADERS, data={}, verify=False)
        # print(resp.text)
        return resp.text

def get_all_devices():
    endpoint = DEVICE_ID_ENDPOINT
    xml_data = make_request(endpoint=endpoint)
    data_dict = xmltodict.parse(xml_data)

    device_id_dict= {}
    for el in data_dict["devices"]["device"]:
        # print(f'Device ID : {el["id"]} , name : {el["name"]}')
        device_id_dict[el["id"]] = el["name"]
    return device_id_dict

def get_device_rules(device_id):
    endpoint = DEVICE_RULE_ENDPOINT.format(device_id)
    # print(endpoint)
    xml_data = make_request(endpoint=endpoint)
    data_dict = xmltodict.parse(xml_data)
    # pprint(data_dict)
    rule_dict = {}
    try:
        for rule in data_dict["rules"]["rule"]:
            # print(rule["id"], " : ", rule["name"])            
            rule_dict[rule["id"]] = rule["name"]
    except Exception:
        pass 
    return rule_dict


def get_utan_no(device_id, rule_id):
    endpoint = UTAN_NO_ENDPOINT.format(device_id, rule_id)
    xml_data = make_request(endpoint=endpoint)
    data_dict = xmltodict.parse(xml_data)
    comment = data_dict["rules"]["rule"]["comment"]
    if comment:
        utan = re.findall("UTAN : \d\d\d\d\d", comment)
        if len(utan)>0:
            # print("===================")
            # print(utan[0])
            return utan[0]

        else:
            return None
    else:
        return None

if __name__ == "__main__":

    # Getting all the devices
    all_device_dict = get_all_devices()
    print("Device list: \n------------------")
    pprint(all_device_dict)
    print("<<<<<<<<<<<<<<-------------->>>>>>>>>>>>>>\n\n")
    all_device_list = [k for k,v in all_device_dict.items()]
  
      
# 2. for each device get all rules: https://tufin-dev.nml.com/securetrack/api/devices/4/rules
    device_rule_dict = {}
    device_rule_dict_raw = {}
    for device in all_device_list:
        # print(f"device name : {all_device_dict[device]}")
        # print("--------------------")
        res = get_device_rules(device)
        device_rule_dict[device] = [k for k,v in res.items()]
        device_rule_dict_raw[all_device_dict[device]] = res

    print("Device rules: \n------------------")
    pprint(device_rule_dict_raw) 
    print("<<<<<<<<<<<<<<-------------->>>>>>>>>>>>>>\n\n")
        # print([k for k,v in res.items()])     
    # pprint(device_rule_dict)

#3. read utan tag value from comment of rule hhttps://tufin-dev.nml.com/securetrack/api/devices/4/rules/47166
    utan_list = []
    for device_id, rules in device_rule_dict.items():
        for rule_id in rules:
            # print("================")
            res = get_utan_no(device_id, rule_id)
            if res:
                utan_list.append(res)
            # print("--------------------")
    print("Utan lists: \n------------------")
    print(utan_list)


#4. query api for utan owner (utan api) (done) https://api.nmlv.nml.com/v1/devops/utan/33538   needs api key to access this api
#5. for each rule update documentation with tech owner https://tufin-dev.nml.com/securetrack/api/devices/4/rules/47166/documentation
