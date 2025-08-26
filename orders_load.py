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
    ('orders.acquisitions_unit', '/acquisitions-units/units'),
    ('orders.acquisitions_unit_membership', '/acquisitions-units/memberships'),
    ('orders.alert', '/orders-storage/alerts'),
    ('orders.order_invoice_relationship', '/orders-storage/order-invoice-relns'),
    ('orders.order_templates', '/orders/order-templates'),
    ('orders.pieces', '/orders-storage/pieces'),
    ('orders.po_line', '/orders-storage/po-lines'),
    ('orders.purchase_order', '/orders-storage/purchase-orders'),
    ('orders.reporting_code', '/orders-storage/reporting-codes'),
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

