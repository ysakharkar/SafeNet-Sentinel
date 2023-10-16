from fuzzywuzzy import process
import json
import pymongo
from pymongo import MongoClient
import getUserSoftware

cluster = MongoClient("connection string")
db = cluster["test"]
collection = db["test"]

# return the concatenated string of vendor and product name of the configuration given the CPE 2.3 formatted string
def softwareFromCPE(str):
    j = 10
    ret = ""

    # extract vendor name
    while(str[j] != ":"):
        if (str[j] == "_"):
            ret += " "
        else:
            ret += str[j]
        j += 1

    ret += " "
    j += 1

    # extract product name
    while (str[j] != ":"):
        if (str[j] == "_"):
            ret += " "
        else:
            ret += str[j]
        j += 1

    return ret

# return true if cpe match represents that of an application (not hardware or os)
def checkApplication(str):

    # 9th character represents the a, o, or h (we want a for application based on CPE 2.3)
    if(str[8] == "a"):
        return True

    return False

def get_matches(query, choices, limit=1):
    results = process.extract(query, choices, limit=1)
    if (results[0][1] >= 90):
        return results[0][0]

    return None

def get_date(date):
    toReturn = ""

    for i in range(len(date)):
        if (date[i] == "T"):
            break
        else:
            toReturn += date[i]

    return toReturn

# create list of user software
getUserSoftware.getUserSoftware()

mySoftware = []
map = {}

with open("mySoftwares.txt", "r") as f:
    mySoftware = f.read().split("\n")

for i in collection.find():
    configurations = []
    # for each configuration
    for j in i['cve']['configurations']:

        # for each node
        for k in j['nodes']:

            # for each matching cpe, we extract the software name
            for l in k['cpeMatch']:
                if (checkApplication(l['criteria'])):
                    configuration = softwareFromCPE((l['criteria']))
                    match = get_matches(configuration, mySoftware)
                    if (match and match not in configurations):
                        configurations.append(match)

                        if match in map.keys():
                            map.get(match).append(i['cve']['id'] + "!" + "nvd.nist.gov/vuln/detail/" + i['cve']['id'] + "!" + get_date(i['cve']['published']) + "!" + 
                            i['cve']['descriptions'][0]['value'])

                        else:
                            map[match] = []
                            map.get(match).append(i['cve']['id'] + "!" + "nvd.nist.gov/vuln/detail/" + i['cve']['id'] + "!" + get_date(i['cve']['published']) + "!" + 
                            i['cve']['descriptions'][0]['value'])

for key in map.keys():
    currList = map.get(key)

    print(key)

    for value in currList:
        print(value)

    print("\n")