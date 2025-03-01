import requests
import sys
import time
from core import Parser
from config.banner import colors
from requests.auth import HTTPBasicAuth
import json

MAX_RESTRIES =  4

def do_request(url, headers):
    time.sleep(2.5)
    res = requests.get(url, headers=headers, auth=HTTPBasicAuth("ThorfexD", "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"))
    if res.status_code  == 200:
        return (res.json(), "OK")
    elif res.status_code == 403:
        while res.status_code == 403:
            time.sleep(60)
            res = requests.get(url, headers=headers, auth=HTTPBasicAuth("ThorfexD", "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"))
        return (res.json(), "OK")
    elif str(res.status_code).startswith("4"):
        return (None, "BAD_REQUEST")
    else:
        return (None, "ERROR")

def requestPage(url, headers):
    print("Querying: ", url)
    data, status = do_request(url, headers)
    if status == "ERROR":
        for _ in range(MAX_RESTRIES):
            data, status = do_request(url, headers)
            print(status)
            if status == "OK": break
        else:
            print("{RED}\n\n[-] Max retries fetching url data \n{END}".format(**colors))
            
    return (data, status)    
    
