from trouvailles import __version__
from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals
from pyramid.view import view_config

from cornice import Service


info_desc = """\
Indexing Service.
"""


indexer = Service(name='indexer', path='/',
                  description=info_desc)

searcher = Service(name='searcher', path='/search',
                   description=info_desc)


@indexer.post()
def index(request):
    """Index an url.
    """
    db = request.registry.settings['database']
    url = request.json['url']
    db.index(url)
    db.flush()
    return {'success': True}


@indexer.get()
def home(request):
    return {'version': __version__}


@searcher.get()
def search(request):
    db = request.registry.settings['database']
    query = request.GET['query']
    results = list(db.search(query))
    return {'results': results}

