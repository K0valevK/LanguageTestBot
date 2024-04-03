# Migrations

From root

`docker run --rm --network="langbot-network" -v "$(pwd)/database/migrations/statistics_db":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/liquibase.properties update`

`docker run --rm --network="langbot-network" -v "$(pwd)/database/migrations/task_db":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/liquibase.properties update`

# Build docker

From root

`docker build -t database -f database/src/Dockerfile .`

# Run docker

`docker run -d --network="langbot-network" -p 8000:8000 --name database database`
