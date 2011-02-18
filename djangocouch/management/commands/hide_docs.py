"""
This script "hides" documents from the database, by changing their doc type.
It expects a single argument, specifying a line separated list of ids to hide.
Anything in the list will have it's doc_type changed from Something to 
DeletedSomething
"""

from django.core.management.base import LabelCommand, CommandError
from dimagi.utils.couch.database import get_db

DELETED_PREFIX = "Deleted"

class Command(LabelCommand):
    help = "Hides documents from couchdb"
    args = "<file>"
    label = 'data file with docs to hide'
    
    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('Please specify %s.' % self.label)
        file_name = args[0]
        db = get_db()
        already_deleted = []
        updated = []
        missing = []
            
        with open(file_name, "r") as f:
            for line in f:
                docid = line.strip()
                if db.doc_exist(docid):
                    doc = db.get(docid)
                    if not doc["doc_type"].startswith(DELETED_PREFIX):
                        doc["doc_type"] = "%s%s" % (DELETED_PREFIX, doc["doc_type"])
                        updated.append(docid)
                        db.save_doc(doc)
                    else:
                        already_deleted.append(docid)
                else:
                    missing.append(docid)
        print "Deleted: %s, Missing: %s, Skipped (already deleted): %s" % \
            (len(updated), len(missing), len(already_deleted))