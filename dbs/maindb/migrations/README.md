# Generic single-database configuration.

To run migrations for maindb we run the following script from Github Workflow:

```bash
 ./.github/scripts/run_db_migrations.sh "alembic upgrade head" ./dbs/maindb/ dev <your-ssm-instance-id>