-- +goose Up
CREATE TABLE IF NOT EXISTS transactions (
	id		UUID	PRIMARY KEY,
	remarks		text	NOT NULL,
	amount		numeric NOT NULL,
	category	text
);

-- +goose Down
DROP TABLE transactions;
