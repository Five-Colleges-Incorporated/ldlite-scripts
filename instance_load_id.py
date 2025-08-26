import os
import sys

import ldlite

ld = ldlite.LDLite()
ld.set_folio_max_retries(6)

ld.connect_folio(
    url=os.environ['FOLIOURL'],
    tenant=os.environ['FOLIOTENANT'],
    user=os.environ['FOLIOUSER'],
    password=os.environ['FOLIOPASSWORD'],
)
db = ld.connect_db_postgresql(dsn=f"""
    dbname={os.environ['PGDATABASE']}
    host={os.environ['PGHOST']}
    port={os.environ['PGPORT']}
    user={os.environ['PGUSER']}
    password={os.environ['PGPASSWORD']}
""")

queries = [
    ('inventory.instance', '/instance-storage/instances'),

#    ('inventory.instance', '/instance-storage/instances', allrec),
#    ('inventory.instance_format', '/instance-formats', allrec),
#    ('inventory.instance_note_type', '/instance-note-types', allrec),
#    ('inventory.instance_relationship', '/instance-storage/instance-relationships', allrec),
#    ('inventory.instance_relationship_type', '/instance-relationship-types', allrec),
#    ('inventory.instance_status', '/instance-statuses', allrec),
#    ('inventory.instance_type', '/instance-types', allrec)
    ]


tables = []
for q in queries:
    try:
        t = ld.query(table=q[0], path=q[1], keep_raw=False)
        tables += t
    except (ValueError, RuntimeError):
        print('folio_demo.py: error processing "' + q[1] + '"', file=sys.stderr)
print()
print('Tables:')
for t in tables:
    print(t)
print('(' + str(len(tables)) + ' tables)')

