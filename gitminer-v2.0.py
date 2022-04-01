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


MAX_PAGE = 100
class GitMiner(object):

    def __init__(self):
        self.description = bn.banner()
        self.seen_links = set()
        parser = argparse.ArgumentParser(self.description)
        parser.add_argument('-q', '--query', metavar='{BLUE}"filename:shadow path:etc"{END}'.format(**colors),
                            help='{YELLOW}Specify search term{END}'.format(**colors), required=True)
        parser.add_argument('-o', '--output', metavar='{BLUE}result.txt{END}'.format(**colors),
                            help='{YELLOW}Specify the output file where it will be saved{END}'.format(**colors),
                            default=None)
        self.args = parser.parse_args()

        if self.args.query is None: 
            os.system('cls' if os.name == 'nt' else 'clear')
            parser.print_help()
            exit()
        self.search_term = requote_uri("/search/code?q=%s&per_page=10" % self.args.query)

    def persist_repos(self, repos, file):
        print("peristing repos", repos)
        for link in repos:
            if file is not None:
                file.write(link)
                file.write('\n')
                file.flush()
                
    def save_repos(self, data, file):
        print("total repo " , len(data["items"]))
        repo_links = map(lambda x: x['repository']['html_url'], data['items'])
        repo_links_filtered = []
        for link in repo_links:
            if not link in self.seen_links:
                self.seen_links.add(link)
                repo_links_filtered.append(link)
        self.persist_repos(repo_links_filtered, file)
        
    def start(self):
        filename = self.args.output
        url_search = Parser.GITHUB_URL + self.search_term
        headers_github = headers.get_headers(url_search)
        headers_github['Accept'] = ''
        
        with open(filename, 'a') as file:
            self.parser = Parser(headers_github, file)
            for i in range(1, MAX_PAGE):
                data, status = requestPage(url_search + "&page=" + str(i), headers_github )
                print("status", status)
                if status == "OK":
                    self.save_repos(data, file)
                    


try:
    GitMiner().start()
except KeyboardInterrupt:
    print("{RED}\n\nBye Bye ;){END}".format(**colors))
    exit()
