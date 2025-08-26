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
    ('agreements.entitlement', '/erm/entitlements'),
   # ('agreements.erm_resource', '/erm/resource'),
    ('agreements.org', '/erm/org'),
    ('agreements.refdata_value', '/erm/refdata'),
    ('agreements.sas', '/erm/sas', 2),
#    ('agreements.usage_data_provider', '/usage-data-providers'),
#    ('finance.fund_code_exp_cla', '/finance/fund-codes-expense-classes'),
    ]

tables = []
for q in queries:
    try:
        if len(q) == 3:
            t = ld.query(table=q[0], path=q[1], json_depth=q[2], keep_raw=False)
        else:
            t = ld.query(table=q[0], path=q[1], keep_raw=False)
        tables += t
    except (ValueError, RuntimeError):
        print('folio_demo.py: error processing "' + q[1] + ' -  ' + q[2] + '"', file=sys.stderr)
print()
print('Tables:')
for t in tables:
    print(t)
print('(' + str(len(tables)) + ' tables)')

