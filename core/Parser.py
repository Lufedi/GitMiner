import sys
import time

from lxml import html

from core.sendRequest import requestPage
from config.banner import colors

MAX_RETRIES = 5

sys.path.append('../')
sys.setrecursionlimit(1048576)


class Parser(object):
    # XPATH QUERIES
    PAGINATION = '//div[contains(@class, "pagination")]/a/text()'
    URL_FILE = '//*[@id="code_search_results"]/div[*]/div[*]/div/div[2]/a/@href'
    NEXT_PAGE = '//a[contains(@class, "next_page")]/@href'
    # URL GITHUB
    GITHUB_URL = 'https://api.github.com'
    GITHUB_RAW_URL = 'https://raw.githubusercontent.com'

    def __init__(self, headers, file):
        self.headers = headers
        self.file = file

        self.seen_urls = set()

    @staticmethod
    def long_sleep(seconds):
        print("{RED}\n[Exceeded rate limit, waiting for {}s]{END}".format(seconds, **colors))
        bar_size = 50

        for i in range(1, seconds + 1):
            progress = i / seconds
            sys.stdout.write("\r{BLUE}[{:50} {}-{}s] {:.0%}{END}".format(
                '=' * int(progress * bar_size), i, seconds, progress, **colors
            ))
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write('\n')

    @staticmethod
    def get_num_pages(content):
        tree = html.fromstring(content)
        number_page = tree.xpath(Parser.PAGINATION)
        if number_page:
            return number_page[len(number_page) - 2]
        else:
            return "1"

    def save_link(self, link):
        if self.file is not None:
            self.file.write(link)
            self.file.write('\n')

    def search(self, url, current_retry):
        content = requestPage(self.GITHUB_URL + url, self.headers, self.cookie).content
        tree = html.fromstring(content)
        url_file = tree.xpath(self.URL_FILE)
        next_page = tree.xpath(self.NEXT_PAGE)
        repos_per_page = len(url_file)
        current_page = url.split("&")[1].split("=")[1]

        if not next_page or len(next_page) < 0:
            if "You have exceeded a secondary rate limit" in str(content):
                self.long_sleep(60)
                self.search(url, 0)
            else:
                exit()

        if repos_per_page == 0:
            if current_retry < MAX_RETRIES:
                print("{RED}\n+[No repositories found in page {}] Retrying {}/{}{END}: ".format(
                    current_page, current_retry + 1, MAX_RETRIES, **colors
                ))
                self.search(url, current_retry + 1)
            else:
                self.search(next_page[0], 0)
        else:
            print(("{YELLOW}\n+[PAGE {}/{}]-----------------------------------------+{END}\n" +
                   "{GREEN}[Repositories found in this page: {}]{END}: ").format(
                current_page, self.total_pages, repos_per_page, **colors
            ))

            for number_url in range(repos_per_page):
                repo_url = self.GITHUB_URL + url_file[number_url].split("/blob")[0]
                if repo_url not in self.seen_urls:
                    user = url_file[number_url].split("/")[1]
                    print("{GREEN}[+]{END} {BLUE}USER{END}: {}".format(user, **colors))
                    print("{GREEN}[+]{END} {BLUE}LINK{END}: {}\n".format(repo_url, **colors))
                    self.save_link(repo_url)
                    self.seen_urls.add(repo_url)

            self.search(next_page[0], 0)
