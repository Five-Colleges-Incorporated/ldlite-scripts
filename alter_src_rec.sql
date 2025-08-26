DROP TABLE IF EXISTS folio_source_record.records_lb;

CREATE TABLE folio_source_record.records_lb AS
    SELECT __id,
    record_id::uuid AS id,
    'ACTUAL' AS state,
    parsed_record__id::uuid AS matched_id,
--    external_ids_holder__instance_id::uuid AS external_id,
        external_ids_holder__instance_hrid AS external_hrid,
	external_ids_holder__instance_id::uuid AS instance_id
--	external_ids_holder__instance_hrid AS instance_hrid
    FROM folio_source_record.records__t;

CREATE INDEX ON folio_source_record.records_lb (__id);

CREATE INDEX ON folio_source_record.records_lb (id);

CREATE INDEX ON folio_source_record.records_lb (state);

CREATE INDEX ON folio_source_record.records_lb (matched_id);

CREATE INDEX ON folio_source_record.records_lb (instance_id);

CREATE INDEX ON folio_source_record.records_lb (external_hrid);

DROP TABLE IF EXISTS folio_source_record.marc_records_lb;

CREATE TABLE folio_source_record.marc_records_lb AS
    SELECT __id,
           record_id::uuid AS id,
           parsed_record__content AS content
    FROM folio_source_record.records__t;

CREATE INDEX ON folio_source_record.marc_records_lb (__id);

CREATE INDEX ON folio_source_record.marc_records_lb (id);

CREATE INDEX ON folio_source_record.marc_records_lb USING gin (content gin_trgm_ops);


DROP TABLE IF EXISTS folio_source_record.records;
DROP TABLE IF EXISTS folio_source_record.marctab;

