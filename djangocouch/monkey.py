from dimagi.utils.modules import to_function
from couchdbkit.client import Database, Server
import couchdbkit

def default_resource_class():
    from django.conf import settings
    if hasattr(settings, 'COUCHDBKIT_RESOURCE_CLASS'):
        return to_function(settings.COUCHDBKIT_RESOURCE_CLASS,
                           failhard=True)
    else:
        return couchdbkit.resource.CouchdbResource

class PatchedServer(Server):
    # patch the database with our own custom default resource class
    def __init__(self, *args, **kwargs):
        if kwargs.get('resource_class') is None:
            kwargs['resource_class'] = default_resource_class()
        super(PatchedServer, self).__init__(*args, **kwargs)

def patch(resource_class):
    if isinstance(resource_class, basestring):
        resource_class = to_function(resource_class,
                                     failhard=True)
    # monkey patch the couchdbkit database to use our new custom
    # resource whenever it's not explicitly specified
    couchdbkit.client.Server = PatchedServer
    couchdbkit.resource.CouchdbResource = resource_class
