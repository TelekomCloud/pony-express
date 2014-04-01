from urlparse import urlparse


def process_url(url):
    o = urlparse(url)

    # construct base mirror url
