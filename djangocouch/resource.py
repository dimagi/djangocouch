from couchdbkit.resource import CouchdbResource
import logging

class CouchdbResouceHack(CouchdbResource):
    # this is just a proof of concept to test that overriding the
    # resource actually works

    def request(self, *args, **kwargs):
        logging.debug('made a request!')
        return super(CouchdbResouceHack, self).request(*args, **kwargs)

