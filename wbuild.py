#!/usr/bin/env python3


import os
import sys
import http.cookiejar
import logging
import re
import lxml.html
import requests
from requests.exceptions import RequestException, BaseHTTPError
from bs4 import BeautifulSoup
from argparse import ArgumentParser, ArgumentError


ARGS_ERROR_EXIT_CODE = 1
HTTP_ERROR_EXIT_CODE = 2


class HttpUtils:
    class GetPageError(Exception):
        """ The exception raised when smth went wrong in 'get_page' function. """
        def __init__(self, desc, url):
            super().__init__(desc, url)
            self.desc = desc
            self.url = url

        def __str__(self):
            tmpl = 'The error "%s" occured while getting the page %s'
            return tmpl % (self.desc, self.url)

    def __init__(self, cookies_file=None):
        self.cookies_file = cookies_file
        self.session = requests.Session()
        self.load_cookies()
        self.set_headers()

    def load_cookies(self):
        if not self.cookies_file:
            return
        if not os.path.isfile(self.cookies_file):
            raise NameError('Cannot find cookies file %s' % self.cookies_file)
        cookie_jar = http.cookiejar.MozillaCookieJar()
        cookie_jar.load(self.cookies_file)
        self.session.cookies = cookie_jar

    def set_headers(self):
        self.session.headers = {'Accept': 'text/html'}

    def get_page(self, url, utf8=False):
        """ Get HTML page or raise GetPageError exception.

        If content-type header isn't 'text/html' the exception raised as well as
        when download error occured.

        """
        try:
            req = self.session.get(url)
        except (RequestException, BaseHTTPError):
            raise HttpUtils.GetPageError('An exception occured at the http request performing', url)
        if req.status_code != requests.codes['ok']:
            raise HttpUtils.GetPageError('HTTP status code: %d' % req.status_code, url)
        if utf8:
            req.encoding = 'utf-8'
        content_type = req.headers['content-type']
        if content_type.startswith('text/html'):
            return req.text
        else:
            raise HttpUtils.GetPageError('Content type "%s" != "text/html"' % content_type, url)

    @staticmethod
    def full_url(url, context_url):
        """ Get full (absolute) URL from arbitrary URL and page where it placed.

        Assume 'context_url' are full url.

        """
        proto, tail = context_url.split(':', 1)
        context_base = proto + '://' + tail.lstrip('/').split('/', 1)[0]

        if url.startswith('#'):
            context_page = context_url.split('#', 1)[0]
            return context_page + url
        elif url.startswith('//'):
            return proto + ':' + url
        elif url.startswith('/'):
            return context_base.rstrip('/') + '/' + url.lstrip('/')
        elif url.startswith(('http://', 'https://', 'ftp://')):
            return url
        else:
            # Need we support relational link like
            # 'smth.html', './smth.html', or '../smth.html'?
            raise NameError('bad url in \'full_url\':\nurl: ' + url + '\n')


class Notabenoid:
    """ http://notabenoid.org """

    books = {
        'whatif': {
            'url': 'http://notabenoid.org/book/41531',
            'filter_re': r'^what-if #\d+\.? .*$',
        },
        'xkcd': {
            'url': 'http://notabenoid.org/book/45995',
            'filter_re': None,
        },
    }

    def __init__(self, book_name, http_utils):
        self.book_name = book_name
        if self.book_name not in Notabenoid.books.keys():
            raise NameError('Unknown Notabenoid book: ' + self.book_name)
        self.book = Notabenoid.books[book_name]
        self.http_utils = http_utils

    def get_list_of_articles(self, filtering=False):
        articles = []
        html = self.http_utils.get_page(self.book['url'])
        doc = lxml.html.document_fromstring(html)
        links = doc.cssselect('table#Chapters tr td.t a')
        for link in links:
            title = link.text
            url = HttpUtils.full_url(link.get('href'), self.book['url'])
            article = (title, url)
            if filtering and self.book['filter_re']:
                if re.match(self.book['filter_re'], title):
                    articles.append(article)
            else:
                articles.append(article)
        return articles

    def get_original(self, url):
        fragments = []
        html = self.http_utils.get_page(url)
        doc = lxml.html.document_fromstring(html)
        for elem in doc.cssselect('table#Tr td.o div p.text'):
            elem_html = lxml.html.tostring(elem)
            elem_text = BeautifulSoup(elem_html, 'html.parser').text
            fragments.append(elem_text)
        return fragments

    def get_translation(self, url):
        html = self.http_utils.get_page(url)
        doc = lxml.html.document_fromstring(html)
        groups = []
        for group_elem in doc.cssselect('table#Tr td.t'):
            group_id = group_elem.getparent().cssselect('td.o p.info a.ord')[0].text
            group = {
                'fragments': [],
                'id': group_id,
            }
            for elem in group_elem.xpath('./div[@id]'):
                elem_html = lxml.html.tostring(elem.cssselect('p.text')[0])
                text = BeautifulSoup(elem_html, 'html.parser').text
                text = re.sub(r'(^|\n)<-->', '\g<1>    ', text)
                text = re.sub(r'^TODO: replace \'<-->\' with \'    \'\n', '', text)
                text = re.sub(r'\n\[labels\].+\[/labels\]', '', text, flags=re.DOTALL)
                author = elem.cssselect('p.info a.user')[0].text
                rating = int(elem.cssselect('div.rating a.current')[0].text)
                fragment = {
                    'text': text,
                    'author': author,
                    'rating': rating,
                }
                group['fragments'].append(fragment)
            groups.append(group)
        return groups


def get_args():
    """ Check and get arguments. Exit with a message when smth went wrong. """
    description = 'The tool for grabbing Russian translation of What If? articles from Notabenoid.'
    parser = ArgumentParser(description=description)
    parser.add_argument('--all', action='store_true',
        help='Print list of articles, originals and all translations\' variants. \n' +
        'By default only last of top rated translations\' variants will be printed.')
    parser.add_argument('cookies_file')
    try:
        args = parser.parse_args()
    except ArgumentError as exc:
        logging.critical(str(exc))
        parser.print_usage(file=sys.stderr)
        exit(ARGS_ERROR_EXIT_CODE)
    return args


def main():
    args = get_args()
    http_utils = HttpUtils(cookies_file=args.cookies_file)
    try:
        notabenoid = Notabenoid('whatif', http_utils)
    except HttpUtils.GetPageError as exc:
        logging.critical(str(exc))
        exit(HTTP_ERROR_EXIT_CODE)
    articles = notabenoid.get_list_of_articles(filtering=True)
    if args.all:
        for article in articles:
            print(str(article))
        print('')
    last_article = articles[0]
    if args.all:
        fragments = notabenoid.get_original(last_article[1])
        for fragment in fragments:
            print(fragment + '\n')
    groups = notabenoid.get_translation(last_article[1])
    for i, group in enumerate(groups):
        maybe_newline = ('\n' if i < len(groups) - 1 else '')
        if args.all:
            for fragment in group['fragments']:
                print(fragment['text'])
                print('%s %s %d%s' % (group['id'], fragment['author'],
                    fragment['rating'], maybe_newline))
        else:
            top_rating = 0
            last_top_rated = None
            for fragment in group['fragments']:
                if fragment['rating'] >= top_rating:
                    last_top_rated = fragment
            print(fragment['text'] + maybe_newline)


if __name__ == '__main__':
    main()
