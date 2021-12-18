import requests
import json


def placeholder_scan_logic():
    f = open('vulns.json','r')
    data = json.loads(f.read())
    return data



def post_vulns(project_id):
    for vuln in placeholder_scan_logic():
        print(requests.post('http://localhost:8000/'+'user/'+str(project_id)+"/"+"vulnerabilities",json=vuln).text)
