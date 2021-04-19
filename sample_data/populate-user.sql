DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id serial PRIMARY KEY NOT NULL,
    username varchar(20),
    email varchar(50),
    password char(60),
    reputation bigint
);

INSERT INTO users
VALUES (1,
        'krumpli',
        'paprikas@krumpli.com',
        '$2b$12$8poW6vXMV7cQiZL7fe1vgeTVo/piZGw3qMhelzaKgcL2tvfrMcuHm',
        10),
       (2,
        'wololo',
        'aom@numba1.com',
        '$2b$12$8poW6vXMV7cQiZL7fe1vgeTVo/piZGw3qMhelzaKgcL2tvfrMcuHm',
        20);