# -*- coding: utf-8 -*-
import argparse
import codecs
import os

from requests.utils import requote_uri

from config import banner as bn
from config import headers
from config.banner import colors
from core.Parser import Parser
from core.sendRequest import requestPage

os.system('cls' if os.name == 'nt' else 'clear')
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

try:
    raw_input  # Python 2
except NameError:
    raw_input = input  # Python 3


class GitMiner(object):

    def __init__(self):
        self.description = bn.banner()
        parser = argparse.ArgumentParser(self.description)
        parser.add_argument('-q', '--query', metavar='{BLUE}"filename:shadow path:etc"{END}'.format(**colors),
                            help='{YELLOW}Specify search term{END}'.format(**colors), required=True)
        parser.add_argument('-o', '--output', metavar='{BLUE}result.txt{END}'.format(**colors),
                            help='{YELLOW}Specify the output file where it will be saved{END}'.format(**colors),
                            default=None)
        parser.add_argument('-c', '--cookie', metavar='{BLUE}cookie.txt{END}'.format(**colors), default=None,
                            required=True)
        self.args = parser.parse_args()

        if self.args.query is None or self.args.cookie is None:
            os.system('cls' if os.name == 'nt' else 'clear')
            parser.print_help()
            exit()
        with open(self.args.cookie) as txt:
            for line in txt:
                self.cookie = headers.parse_cookie(line)
        self.search_term = requote_uri("/search?o=desc&p=1&q=%s&s=indexed&type=Code" % self.args.query)

    def start(self):
        print(self.description)
        filename = self.args.output
        url_search = Parser.GITHUB_URL + self.search_term
        headers_github = headers.get_headers(url_search)

        content_html = requestPage(url_search, headers_github, self.cookie)

        with open(filename, 'a') as file:
            total_pages = Parser.get_num_pages(content_html.content)
            p = Parser(headers_github, self.cookie, file, total_pages)
            p.search(self.search_term, 0)


try:
    GitMiner().start()
except KeyboardInterrupt:
    print("{RED}\n\nBye Bye ;){END}".format(**colors))
    exit()
