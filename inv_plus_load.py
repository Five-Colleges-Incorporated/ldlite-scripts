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
    ('invoice.invoice_lines', '/invoice/invoice-lines'),
    ('invoice.invoices', '/invoice/invoices'),
    ('invoice.batch_groups', '/batch-groups'),
    ('invoice.batch_voucher_exp', '/batch-voucher/batch-voucher-exports'),
    ('invoice.voucher_lines', '/voucher/voucher-lines'),
    ('invoice.vouchers', '/voucher/vouchers'),
    ('licenses.license', '/licenses/licenses'),
    ('notes.note_data', '/notes'),
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

