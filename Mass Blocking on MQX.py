import os
import pandas as pd
import requests
import json

def read_client_secrets(file_path):
    client_secrets = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            client_secrets[key] = value
    return client_secrets

# Read client secrets
client_secrets = read_client_secrets('/Users/oliver/client.txt')

headers1 = {
    'content-type': 'application/x-www-form-urlencoded',
}

data = {
  'client_secret': client_secrets['client_secret'],
  'client_id': client_secrets['client_id'],
  'grant_type': 'client_credentials'
}

response = requests.post('https://auth.smaato.com/v2/auth/token/', headers=headers, data=data)
v = response.json()
w = v['access_token']

print(w)


block_info = pd.read_csv('/Users/oliver/Downloads/Untitled spreadsheet - Sheet1.csv')

url = "https://mqx-api.smaato.com/ad-quality/events/violations/"
headers = {"Authorization":'Bearer {}'.format(w), "Content-Type": "application/json"}

body = {"comment": "flagged by anyclip",
        "violation_type": "other",
        #"block_rule_targeting": {"multipliers": [203]},
        "block_rule_targeting":
           {"publishers": [1100053957]},
         #{"block_all": True},
        "campaign_id": "*",
        "creative_id": "*",
        "dsp_id": "1001044",
        "evidence_url": "",
        "scanner": "manual",
        "seat_id": "429"
        }
fail_array = []
# for i in range(2):
for i in range(len(block_info)):
    print(i)
    #body["dsp_id"] = int(block_info["dpid"][i])
    #body["campaign_id"] = str(block_info["cid"][i])
    #body["creative_id"] = str(block_info["crid"][i])
    #body["seat_id"]     = str(block_info["seatid"][i])
    json_body = json.loads(json.dumps(body))
    send_req = requests.post(url, headers=json.loads(json.dumps(headers)), json=json_body)
    print(send_req.status_code)
    print("")
    if (send_req.status_code != 201):
        fail_array.append(i)