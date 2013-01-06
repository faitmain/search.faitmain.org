import os
import xappy
from BeautifulSoup import BeautifulSoup
import urllib2


def extract_content(url):
    # XXX for now just the body text
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    body = soup.body(text=True)

    # XXX maybe should let Xapian do this.
    body = [line.strip() for line in body if line.strip() not in ('\n', '')]
    body = ' '.join(body)
    body = body.replace('\n', '')
    body = body.encode('utf8')
    return body


def create_index(dbpath):
    conn = xappy.IndexerConnection(dbpath)
    try:
        conn.add_field_action('url', xappy.FieldActions.STORE_CONTENT)
        conn.add_field_action('url', xappy.FieldActions.INDEX_EXACT)
        conn.add_field_action('text', xappy.FieldActions.STORE_CONTENT)
        conn.add_field_action('text', xappy.FieldActions.INDEX_FREETEXT, language='fr')
    finally:
        conn.close()


class Database(object):
    def __init__(self, dbpath, create=False):
        if not os.path.exists(dbpath) and create:
            create_index(dbpath)
        self.dbpath = dbpath
        self.conn = xappy.IndexerConnection(dbpath)

    def index(self, url):
        _search = xappy.SearchConnection(self.dbpath)
        try:
            query = _search.query_field('url', url)
            results = _search.search(query, 0, 10)
            if len(results) > 0:
                # already indexed
                print('%r already indexed' % url)
                return
        finally:
            _search.close()

        content = extract_content(url)
        doc = xappy.UnprocessedDocument()
        doc.fields.append(xappy.Field('url', url))
        doc.fields.append(xappy.Field('text', content))
        self.conn.add(doc)

    def flush(self):
        self.conn.flush()

    def search(self, query):
        # XXX pool ?
        _search = xappy.SearchConnection(self.dbpath)
        try:
            query = _search.query_parse(query,
                                         default_op=_search.OP_AND)
            results = _search.search(query, 0, 10)
            for result in results:
                yield result.data['url'][0]
        finally:
            _search.close()


if __name__ == '__main__':
    db = Database('/tmp/ok', create=True)
    db.index('http://faitmain.org/janvier-2013/wtf.html')
    db.flush()

    for res in db.search('San Francisco'):
        print res
