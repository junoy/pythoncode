#!/usr/bin/env python
#coding=utf8
 
try:
    import os
    import urllib
    import pycurl
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    from pyquery import PyQuery as pyq
 
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
 
except ImportError:
    print >> sys.stderr, """\
 
There was a problem importing one of the Python modules required.
The error leading to this problem was:
 
%s
 
Please install a package which provides this module, or
verify that the module is installed correctly.
 
It's possible that the above module doesn't match the current version of Python,
which is:
 
%s
 
""" % (sys.exc_info(), sys.version)
    sys.exit(1)
 
 
__prog__ = "crawl"
__site__ = "http://www.oschina.net/code"
__version__ = "1.0"
 
 
class HttpRequest(object):
    curl = None
    def __init__(self):
        self.url = None
        self.url_para = None
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.VERBOSE, 0)
 
        self.curl.setopt(pycurl.USERAGENT, 'Miozilla/4.0 (compatible; MSIE 8.0; WindowsNT 6.1)')
        self.curl.setopt(pycurl.HEADER, 1)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        self.curl.setopt(pycurl.COOKIEFILE, 'cookie.dat')
        self.curl.setopt(pycurl.COOKIEJAR, 'cookie.dat')
        self.curl.setopt(pycurl.HTTPGET, 1)
        self.curl.setopt(pycurl.ENCODING, 'gzip,deflate')
        self.curl.setopt(pycurl.CONNECTTIMEOUT, 60)
        self.curl.setopt(pycurl.TIMEOUT, 300)
 
    def set_url_para(self, para):
        self.url_para = para
        url = self.url + para
        self.curl.setopt(pycurl.URL, url)
 
    def set_post_para(self, para):
        self.curl.setopt(pycurl.POST, 1)
        self.curl.setopt(pycurl.POSTFIELDS, urllib.urlencode(para))
 
    def set_cookie(self, cookie):
        self.curl.setopt(pycurl.COOKIE, cookie)
 
    def dry_write(self, buf):
        pass
 
    def download(self, url, file_path):
        dir = os.path.dirname(file_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.HEADER, False)
        self.curl.setopt(pycurl.HEADERFUNCTION, self.dry_write) #忽略包头信息，否则会写入文件?!
        with open(file_path, 'wb') as outfile:
            self.curl.setopt(pycurl.WRITEFUNCTION, outfile.write)
            try:
                self.curl.perform()
            except Exception, e:
                self.curl.close()
 
    def perform(self, url, referer=''):
        assert url, 'url is null!'
        self.curl.setopt(pycurl.URL, url)
        referer and self.curl.setopt(pycurl.REFERER, referer)
 
        self.buf = StringIO()
        self.head = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, self.buf.write)
        self.curl.setopt(pycurl.HEADERFUNCTION, self.head.write)
        try:
            self.curl.perform()
            self.r = self.buf.getvalue()
            self.h = self.head.getvalue()
            self.code = self.curl.getinfo(pycurl.HTTP_CODE)
            self.info = self.curl.getinfo(pycurl.EFFECTIVE_URL)
            self.cookie = self.curl.getinfo(pycurl.INFO_COOKIELIST)
 
            self.curl.setopt(pycurl.REFERER, self.info) #AUTO REFERER
        except Exception, e:
            self.curl.close()
        self.buf.close()
        self.head.close()
 
    def __del__(self):
        self.curl.close()
 
    def get_body(self):
        return self.r
    def get_head(self):
        return self.h
    def get_code(self):
        return self.code
    def get_info(self):
        return self.info
    def get_cookie(self):
        return self.cookie
 
if __name__ == '__main__':
 
    asp_range = xrange(1, 10)
    page_range = xrange(1, 10)
    crawl = HttpRequest()
    for i in asp_range:
        for j in page_range:
            url = 'http://www.nbbicycle.com/html/116/s%d.asp?i=1&page=%d' % (i, j)
            try:
                crawl.perform(url)
                doc = pyq(crawl.get_body())
                content = doc('.contd')
                print content.children('div').eq(0).text()
                for tr in content.items('tr'):
                    print tr.text()
            except Exception, e:
                print e