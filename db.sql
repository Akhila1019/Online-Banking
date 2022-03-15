CREATE TABLE credentials (
uid serial PRIMARY KEY,
username VARCHAR(25) not null unique,
pwdhash VARCHAR(250) not null
);

SELECT * FROM credentials;

--  DROP TABLE credentials;
-- DELETE FROM credentials;

CREATE TABLE users(
uid serial PRIMARY KEY,
account_number VARCHAR(50) not null unique,
cif_number VARCHAR(50) not null unique,
branch_code INTEGER not null,
country VARCHAR(50) not null,
phone  BIGINT not null,
facility VARCHAR(100) not null
);

SELECT * FROM users;

-- DROP TABLE users;
-- DELETE FROM users;