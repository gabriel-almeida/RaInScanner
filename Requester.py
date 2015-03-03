__author__ = 'Gabriel'
import re
import hashlib
import urllib.request
import datetime

FIREFOX_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
HTTP_PROTOCOL = 'http://'
TITLE_TAG_REGEXP = "<title>(.+?)</title>"
DEFACE_REGEXP = re.compile("h[a4]ck[e3]d[ by]?", re.IGNORECASE)


def is_defaced(page):
    if DEFACE_REGEXP.search(page):
        return True
    return False


class PageAnaliser():
    def __init__(self, save_criteria=is_defaced):
        self._save_criteria = save_criteria
        self._results = dict()

    def analise(self, url, page):
        title_search = re.compile(TITLE_TAG_REGEXP).search(page)
        title = ''
        if title_search is not None:
            title = title_search.group(1)

        byte_page = str.encode(page)

        obj_md5 = hashlib.md5()
        obj_md5.update(byte_page)
        str_md5 = obj_md5.hexdigest()

        obj_sha1 = hashlib.sha1()
        obj_sha1.update(byte_page)
        str_sha1 = obj_sha1.hexdigest()

        save = ''
        if self._save_criteria(page):
            save = page

        out_tuple = (url, title, str_md5, str_sha1, save, str(datetime.datetime.now()))
        self._results[url] = out_tuple

        return out_tuple


class WebRequester():
    def __init__(self, useragent=FIREFOX_AGENT, timeout=5, analiser=PageAnaliser()):
        self._headers = {'UserAgent': useragent}
        self._timeout = timeout
        self._analiser = analiser

    def request(self, url):
        url = url.strip()
        if not url.startswith(HTTP_PROTOCOL):
            url = HTTP_PROTOCOL + url
        try:
            req = urllib.request.Request(url, headers=self._headers)
            f = urllib.request.urlopen(req, timeout=self._timeout)
            page = f.read().decode('utf8', errors='ignore')
            return self._analiser.analise(url, page)
        except:
            return None


if __name__ == '__main__':
    print(is_defaced('h4ckED hua3hu3hu3hu3uh brbr?'))

    r = WebRequester()
    print(r.request('www.ufrj.br'))
