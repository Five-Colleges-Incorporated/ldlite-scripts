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
    ('inventory.alternative_title_type', '/alternative-title-types'),
    ('inventory.call_number_type', '/call-number-types'),
    ('inventory.classification_type', '/classification-types'),
    ('inventory.contributor_name_type', '/contributor-name-types'),
    ('inventory.contributor_type', '/contributor-types'),
    ('inventory.electronic_access_relationship', '/electronic-access-relationships'),
    ('inventory.identifier_type', '/identifier-types'),
    ('inventory.ill_policy', '/ill-policies'),
    ('inventory.loan_type', '/loan-types'),
    ('inventory.location', '/locations'),
    ('inventory.loccampus', '/location-units/campuses'),
    ('inventory.locinstitution', '/location-units/institutions'),
    ('inventory.loclibrary', '/location-units/libraries'),
    ('inventory.material_type', '/material-types'),
    ('inventory.mode_of_issuance', '/modes-of-issuance'),
    ('inventory.nature_of_content_term', '/nature-of-content-terms'),
    ('inventory.service_point', '/service-points'),
    ('inventory.service_point_user', '/service-points-users'),
    ('inventory.statistical_code', '/statistical-codes'),
    ('inventory.statistical_code_type', '/statistical-code-types'),
    ('inventory.bound_width_parts', '/inventory-storage/bound-with-parts'),
    ('inventory.instance_relationship', '/instance-storage/instance-relationships'),
    ('inventory.instance_relationship_type', '/instance-relationship-types'),
    ('inventory.preceding_suceeding_titles', '/preceding-succeeding-titles'),
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

