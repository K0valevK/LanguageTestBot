# Build docker

From root

`docker build -t bot -f bot/src/Dockerfile .`

# Run docker

`docker run -d --network="langbot-network" --name bot bot`
