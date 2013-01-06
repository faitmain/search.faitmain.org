from collections import defaultdict

from pyramid.exceptions import Forbidden
from pyramid.security import authenticated_userid, effective_principals
from pyramid.view import view_config

from cornice import Service


info_desc = """\
Indexing Service.
"""


indexer = Service(name='indexer', path='/indexing',
                  description=info_desc)


@indexer.post()
def index(request):
    """Index an url.
    """
    # TODO
    return {'success': True}
