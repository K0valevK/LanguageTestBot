# Build docker

From root

`docker build -t logs -f logger_db/src/Dockerfile .`

# Run docker

`docker run -d --network="langbot-network" --name logs logs`
