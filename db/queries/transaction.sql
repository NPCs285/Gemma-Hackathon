-- name: GetTransaction :many
SELECT * FROM transactions;

-- name: InsertTransaction :exec
INSERT INTO transactions(id,remarks,amount, category) 
VALUES($1,$2,$3,$4);
