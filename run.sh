#!/bin/bash

ENV_FILE=".env"

export $(cat .env | xargs)

DB_HOST="db"
sqlc generate
goose postgres -dir ./db/schema/ "postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}" up
