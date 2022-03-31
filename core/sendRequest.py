import requests
import sys
import time
from core import Parser
from config.banner import colors


def requestPage(url, headers, cookie):
    time.sleep(2)
    req = requests.get(url, headers=headers, cookies=cookie)
    if " find any code matching" in req.text:
        print("{RED}\n\n[-] We couldn't find any code matching \n{END}".format(**colors))
        sys.exit()
    return req
