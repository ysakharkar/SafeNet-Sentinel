from datetime import datetime, timedelta
import requests
import json
import pymongo
from pymongo import MongoClient

cluster = MongoClient("connection string")
db = cluster["test"]
collection = db["collection"]

posts = []

today = datetime.now().date()

yesterday = today - timedelta(days=1)
ten_days_ago = today - timedelta(days=10)

base = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
startDate = "?pubStartDate=" + str(ten_days_ago) + "T00:00:00.000" 
endDate = "&pubEndDate=" + str(yesterday) + "T00:00:00.000"

req = requests.get(base + startDate + endDate)
obj = req.json()

totalResults = obj['totalResults']
startIndex = 0

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

def hasApplication(entry):
    # for each configuration
    for j in i['cve']['configurations']:

        # for each node
        for k in j['nodes']:

            # for each matching cpe, we extract the software name
            for l in k['cpeMatch']:
                if (checkApplication(l['criteria'])):
                    return True
    
    return False

def alreadyExists(id):
    if(collection.count_documents({"cve.id": id}) > 0):
        print(f'{id} already exists')
        return True

    print(f'{id} doesn\'t already exist, so we will add it')
    return False

while (True):
    print(totalResults)
    print(startIndex)
    # for each CVE
    for i in obj['vulnerabilities']:
        print('NEW CVE: ' + i['cve']['id'])

        # if it's been analyzed
        if (i['cve']['vulnStatus'] == "Analyzed"):
            if (hasApplication(i) and not alreadyExists(i['cve']['id'])):
                posts.append(i)

    # update to continue paging through all results
    totalResults -= 2000
    startIndex += 2000

    # if totalResults ever equals or goes below 0, we've paged through all the results for the dates
    if (totalResults > 0):
        print('requesting' + base + startDate + endDate + "&startIndex=" + str(startIndex))
        req = requests.get(base + startDate + endDate + "&startIndex=" + str(startIndex))
        obj = req.json()
    else:
        break

collection.insert_many(posts)

