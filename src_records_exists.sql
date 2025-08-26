SELECT COUNT(*) FROM information_schema.tables 
WHERE
    table_schema = 'folio_source_record' AND 
    table_name = 'records__t';
