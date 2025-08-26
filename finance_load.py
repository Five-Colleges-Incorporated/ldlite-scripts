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
    ('finance.budget', '/finance/budgets'),
    ('finance.expense_class', '/finance/expense-classes'),
#    ('finance.fund_code_exp_cla', '/finance/fund-codes-expense-classes'),
    ('finance.fiscal_year', '/finance/fiscal-years'),
    ('finance.fund', '/finance/funds'),
    ('finance.fund_type', '/finance/fund-types'),
    ('finance.group_fund_fy', '/finance/group-fund-fiscal-years'),
##    ('finance.group_fy_sum', '/finance/group-fiscal-year-summaries'),
    ('finance.groups', '/finance/groups'),
    ('finance.ledger_roll_budget', '/finance/ledger-rollovers-budgets'),
    ('finance.ledger_roll_log', '/finance/ledger-rollovers-logs'),
#    ('finance.ledger_roll_error', '/finance/ledger-rollovers-errors'),
#    ('finance.ledger_roll', ' /finance/ledger-rollovers'),
    ('finance.ledger_roll_prog', '/finance/ledger-rollovers-progress'),
    ('finance.ledger', '/finance/ledgers'),
    ('finance.transaction', '/finance/transactions'),
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

