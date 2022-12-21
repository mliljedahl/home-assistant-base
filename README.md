# home-assistant-base

Sets up Home Assistant and multiple integrations using docker-compose.

# Sensitive data map

Script for managing this is in the making.

```
bin/grafana/datasources/influxdb.yml token (same as DOCKER_INFLUXDB_INIT_ADMIN_TOKEN and influxdb_token)
bin/mosquitto/pwfile (user and pass is used in zwave-js integration)
bin/grafana.env GF_DATABASE_PASSWORD (same as POSTGRES_GRAFANA_PASSWORD)
bin/influxdb.env DOCKER_INFLUXDB_INIT_PASSWORD DOCKER_INFLUXDB_INIT_ADMIN_TOKEN (same as token and influxdb_token)
bin/postgres.env POSTGRES_PASSWORD POSTGRES_GRAFANA_PASSWORD (same as GF_DATABASE_PASSWORD)
bin/zwavejs.env SESSION_SECRET
configs/home-assistant/secrets.yaml influxdb_token (same as DOCKER_INFLUXDB_INIT_ADMIN_TOKEN and token) recorder_db
```