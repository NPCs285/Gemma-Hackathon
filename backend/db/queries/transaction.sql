-- name: GetTransactionLimit :many
SELECT * FROM transactions
LIMIT $1;

-- name: GetAllTransaction :many
SELECT * FROM transactions;

-- name: InsertTransaction :exec
INSERT INTO transactions(id,remarks,amount,transaction_date,category) 
VALUES($1,$2,$3,$4,$5);

-- name: GetByCategory :many
SELECT category, SUM(amount) FROM transactions
GROUP BY category;
