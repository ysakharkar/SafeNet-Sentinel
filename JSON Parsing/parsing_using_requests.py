import requests
import json

req = requests.get("https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate=2023-05-01T00:00:00.000&pubEndDate=2023-07-01T00:00:00.000")
obj = req.json()

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
for i in obj['vulnerabilities']:
    print('NEW CVE: ' + i['cve']['id'])

    # if it's been analyzed
    if (i['cve']['vulnStatus'] == "Analyzed"):

        # for each configuration
        for j in i['cve']['configurations']:

            # for each node
            for k in j['nodes']:

                # for each matching cpe, we extract the software name
                for l in k['cpeMatch']:
                    if (checkApplication(l['criteria'])):
                        print(softwareFromCPE((l['criteria'])))
                        print('\n')


    