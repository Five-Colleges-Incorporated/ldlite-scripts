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
    ('circulation.cancellation_reason', '/cancellation-reason-storage/cancellation-reasons'),
    ('circulation.fixed_due_date_schedule', '/fixed-due-date-schedule-storage/fixed-due-date-schedules'),
    ('circulation.loan', '/loan-storage/loans'),
    ('circulation.loan_policy', '/loan-policy-storage/loan-policies'),
    ('circulation.patron_action_session', '/patron-action-session-storage/patron-action-sessions'),
    ('circulation.patron_notice_policy', '/patron-notice-policy-storage/patron-notice-policies'),
    ('circulation.request', '/request-storage/requests'),
    ('circulation.request_policy', '/request-policy-storage/request-policies'),
    ('circulation.scheduled_notice', '/scheduled-notice-storage/scheduled-notices'),
    ('circulation.staff_slips', '/staff-slips-storage/staff-slips'),
    ('circulation.user_request_preference', '/request-preference-storage/request-preference'),
    ('configuration.config_data', '/configurations/entries'),
    ('circulation.email_notices', '/email'),
    ('circulation.manualblocks', '/manualblocks'),
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

