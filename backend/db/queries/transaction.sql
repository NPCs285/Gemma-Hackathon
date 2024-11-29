-- name: GetTransaction :many
SELECT * FROM transactions
LIMIT = $1;

-- name: InsertTransaction :exec
INSERT INTO transactions(id,remarks,amount, category) 
VALUES($1,$2,$3,$4);
