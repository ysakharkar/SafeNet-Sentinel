import pymongo
from pymongo import MongoClient
import json

cluster = MongoClient("connection string")
db = cluster["test"]
collection = db["collection"]

# import json

# json_file = open('debug.json', 'r')
# jsondata = json_file.read()

# obj = json.loads(jsondata)


# return true if cpe match represents that of an application (not hardware or os)
def checkApplication(str):

    # 9th character represents the a, o, or h (we want a for application based on CPE 2.3)
    if(str[8] == "a"):
        return True

    return False

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

# for each CVE
# for i in obj['vulnerabilities']:
    # collection.insert_one(i)

    
# results = collection.find({"cve.id":"CVE-2022-30579"})

# for result in results:
   #  print(result)
    # print(" --------- ")

# results = collection.find({"cve.id": "CVE-2023-3469"})
results = collection.count_documents({"cve.id": "CVE-2023-36868"})
print(results)
