FROM golang:1.23.3-alpine3.20
WORKDIR /app
RUN  go install github.com/sqlc-dev/sqlc/cmd/sqlc@latest
RUN  go install github.com/pressly/goose/v3/cmd/goose@latest
CMD ["/bin/sh", "/app/run.sh"]
