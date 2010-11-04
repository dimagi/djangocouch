import logging
from django.conf import settings
from django.core.management.base import LabelCommand
from dimagi.utils.couch.database import get_db, get_view_names
from datetime import datetime

class Command(LabelCommand):
    help = "Listens for patient conflicts and resolves them."
    args = ""
    label = ""
     
    def handle(self, *args, **options):
        db = get_db()
        
        for view in get_view_names(db):
            starttime = datetime.now()
            logging.debug("reindexing view: %s" % view)
            print "reindexing view: %s" % view
            try:
                for val in db.view(view):
                    # we have to call it once, simulated by iterating to the first element
                    break
            except Exception, e:
                logging.error("Problem reindexing view %s" % view)
            
            logging.debug("Elapsed time for %s: %s" % (view, datetime.now() - starttime))
            print ("Elapsed time for %s: %s" % (view, datetime.now() - starttime))

            
                
    def __del__(self):
        pass
    
