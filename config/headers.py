# -*- coding: utf-8 -*-
def get_headers(referer):
    return {
            "Accept": "application/vnd.github.v3+json",
            }

def get_headers_raw():
    return {"Host": "raw.githubusercontent.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}


def parse_cookie(cookie):
    parsed_cookie = {}
    for line in cookie.split(";"):
        param = line.strip().split("=")[0]
        values = line.strip().split("=")[1]
        parsed_cookie.update({param: values})

    return parsed_cookie
