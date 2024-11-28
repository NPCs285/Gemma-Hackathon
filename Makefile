up:
	@goose postgres -dir ./db/schema/ "postgres://postgres:postgres@localhost:5432/tracker" up

down:
	@goose postgres -dir ./db/schema/ "postgres://postgres:postgres@localhost:5432/tracker" down
