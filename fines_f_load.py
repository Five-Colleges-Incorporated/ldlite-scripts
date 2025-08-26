import os
import sys

import ldlite

ld = ldlite.LDLite()

import os
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
    ('feesfines.accounts', '/accounts'),
    ('feesfines.comments', '/comments'),
    ('feesfines.feefineactions', '/feefineactions'),
    ('feesfines.feefines', '/feefines'),
    ('feesfines.lost_item_fee_policy', '/lost-item-fees-policies'),
    ('feesfines.manualblocks', '/manualblocks'),
    ('feesfines.overdue_fine_policy', '/overdue-fines-policies'),
    ('feesfines.owners', '/owners'),
    ('feesfines.payments', '/payments'),
    ('feesfines.refunds', '/refunds'),
    ('feesfines.transfer_criteria', '/transfer-criterias'),
    ('feesfines.transfers', '/transfers'),
    ('feesfines.waives', '/waives'),
    ('feesfines.actual_cost_record', '/actual-cost-record-storage/actual-cost-records'),
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

