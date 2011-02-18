from django.core.management.base import LabelCommand
from dimagi.utils.couch.database import get_db, get_design_docs
import logging
from optparse import make_option
from dimagi.utils.django.management import are_you_sure
import sys

WARNING = \
"""Compacting views may take a while and might SEVERELY
tie up your system resources during that time. 
This operation is PERMANENT and IRREVERSIBLE.

Are you sure you want to do this? (y/n)  """

class Command(LabelCommand):
    help = "Compacts couch views."
    args = ""
    label = ""
    option_list = LabelCommand.option_list + \
        (make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind. '    \
                 'Databases will be deleted without warning.'),)

    
    def handle(self, *args, **options):
        should_proceed = are_you_sure(WARNING) if options["interactive"] else True
        if not should_proceed:
            print "Ok, aborting"
            sys.exit()
            
        db = get_db()
        for doc in get_design_docs(db):
            logging.debug("compacting views for app: %s" % doc.name)
            print("compacting views for app: %s" % doc.name)
            db.compact(doc.name)
                
    def __del__(self):
        pass
    
