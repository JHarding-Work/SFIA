docker-compose down
docker-compose --env-file variables.env build
echo "Sleeping while mysql database configures..."
docker-compose --env-file variables.env up -d
