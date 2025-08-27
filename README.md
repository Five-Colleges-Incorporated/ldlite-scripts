# Five Colleges Load Scripts

These are the actual scripts that are run on a nightly and weekly basis for loading Five Colleges LDLite database.
The scripts and setup instructions are provided as-is and we make no guarantees as to the completeness, security, stability, or soundness.
That these scripts are maintained by the same human maintaining LDLite itself is purely incidental and there is no association between these scripts and the Library Data Platform organization.

The infrastructure currently used for running these scripts is:
* Cloud Instance for running the Scripts - 2 Shared CPU / 2 GB Memory / 125GB disk
* Cloud Managemed Postgres Instance - 2 Shared CPU / 8 GB Memory / 400GB disk

This costs approximately $2500 a year using DigitalOcean as a cloud provider.

## Rough Performance Numbers

Five Colleges has ~5.5 Million Instance and MARC records, 10 Million Item records, and 5 Million Circulation Log records.
Given the above infrastructure and data sizes, with LDLite v3.1 it takes approximately:
* 4.5 Hours to load the circulation data each night
* 2.5 Hours to load the non-circulation data each night
* 31 Hours to load the Instance, Holdings, and Item data each weekend 
* 20.5 Hours to load the MARC data

We have on average 5-10 concurrent users with "acceptable" analytics query performance.

## Setup

Note, this assumes you've access to a linux server setup more or less normally as well as admin permissions to a postgres database.

1. Create an ldlite directory, we've conventionally used `ldlite-<version>` as the naming convention to be able to compare multiple LDLite versions.
1. [Install UV](https://docs.astral.sh/uv/getting-started/installation/), an extremely fast Python package and project manager written in Rust. Note, you can use any python environment manager by modifying the scripts accordingly. UV is just the simplest we've found.
1. In the directory created in 1. run `uv init` and `uv add ldlite==<version>`.
1. Copy or git clone this repository into the ldlite directory and name it `scripts`.
1. Create a `logs` directory in the ldlite directory.
1. Run crontab -e and add the cron jobs from the crontab file in this repository.
1. Create .env, .folioenv, .pgenv files in the home folder of the cron user. More information is provided below.
1. Follow the instructions for [setting up ldpmarc](https://github.com/library-data-platform/ldlite/blob/main/srs.md#running-ldpmarc) in the LDLite documenation.
1. Create the postgres database, `ldlite` is a good starting name.
1. Create a write postgres user with permissions to create schemas and tables in the postgres database.
1. Create a read-only postgres user, the MARC scripts assume this will be `folio_read` so update them if you use something else.
1. Install pg_trgm with `CREATE EXTENSION pg_trgm;`
1. (Optionally) Give the read-only postgres create/write access to the public schema for saving intermediate results and queries.
1. Tada! Logs of each LDLite script will be written to the logs folder when it runs. Users should login as the read-only user.
1. After the first run, grant USAGE to the read-only postgres user for all the created schemas.
1. After the first run, grant SELECT to the read-only postgres user for all tables in the created schemas.
1. After the first run, as the write postgres user, grant SELECT default permissions to the read-only user for all future tables in the created schemas.

## Sample .env files
Thes files go in the home directory of the user running cron and will be sourced to set the appropriate environment.

#### .env
```
PATH="/path/containing/uv:/path/containing/ldpmarc:$PATH"
```

#### .folioenv
```
FOLIOURL="https://<okapi or eureka url>"
FOLIOTENANT="<tenant, ecs is not supported (yet)>"
FOLIOUSER="<service user with read permissions to all the endpoints to be harvested>"
FOLIOPASSWORD="<service user password>"
```

#### .pgenv
```
PGHOST="<be sure to use the private hostname if running in the cloud to avoid egress costs>"
PGPORT="<port>"
PGDATABASE="<name of the ldlite database>"
PGUSER="<postgres user with write permissions to the ldlite database>"
PGPASSWORD="<write postgres user password>"
```
