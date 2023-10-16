from fuzzywuzzy import process
import requests
import json

base = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
startDate = "?pubStartDate=2023-05-01T00:00:00.000" 
endDate = "&pubEndDate=2023-07-01T00:00:00.000"

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

def get_matches(query, choices, limit=1):
    results = process.extract(query, choices, limit=1)
    if (results[0][1] >= 90):
        return results

    return None

mySoftware = []

with open("user_softwares.txt", "r") as f:
    mySoftware = f.read().split("\n")

while (True):
    # for each CVE
    for i in obj['vulnerabilities']:

        # if it's been analyzed
        if (i['cve']['vulnStatus'] == "Analyzed"):

            # for each configuration
            for j in i['cve']['configurations']:

                # for each node
                for k in j['nodes']:

                    # for each matching cpe, we extract the software name
                    for l in k['cpeMatch']:
                        if (checkApplication(l['criteria'])):
                            configuration = softwareFromCPE((l['criteria']))
                            match = get_matches(configuration, mySoftware)
                            if (match):
                                print(match)
                                print("visit nvd.nist.gov/vuln/detail/" + i['cve']['id'])

    # update to continue paging through all results
    totalResults -= 2000
    startIndex += 2000

    # if totalResults ever equals or goes below 0, we've paged through all the results for the dates
    if (totalResults > 0):
        req = requests.get(base + startDate + endDate + "&startIndex=" + str(startIndex))
        obj = req.json()
    else:
        break