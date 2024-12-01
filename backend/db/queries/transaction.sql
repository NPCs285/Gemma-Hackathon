-- name: GetTransactionLimit :many
SELECT * FROM transactions
ORDER BY transaction_date DESC
LIMIT $1
OFFSET $2;

-- name: GetAllTransaction :many
SELECT * FROM transactions;

-- name: InsertTransaction :exec
INSERT INTO transactions(id,remarks,amount,transaction_date,category) 
VALUES($1,$2,$3,$4,$5);

-- name: GetByCategory :many
SELECT category AS name, SUM(amount) AS value FROM transactions
GROUP BY category;
