# Migrations

`docker run --rm --network="langbot-network" -v "$(pwd)/migrations":/app liquibase/liquibase:4.19.0 --defaultsFile=/app/liquibase.properties update`

# Build docker

From root

`docker build -t database -f database/src/Dockerfile .`

# Run docker

`docker run -d --network="langbot-network" -p 8000:8000 database`
