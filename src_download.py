import os
import sys

import ldlite

ld = ldlite.LDLite()

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
    ('folio_source_record.records', '/source-storage/source-records')
    ]

tables = []
for q in queries:
    try:
        t = ld.query(table=q[0], path=q[1], json_depth=2)
        tables += t
    except Exception as e:
        print('folio_src.py: error processing "' + q[1] + '"', file=sys.stderr)
        print(e, file=sys.stderr)
print()
print('Tables:')
for t in tables:
    print(t)
print('(' + str(len(tables)) + ' tables)')

