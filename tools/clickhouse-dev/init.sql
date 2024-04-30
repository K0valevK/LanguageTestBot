CREATE DATABASE IF NOT EXISTS bot;

CREATE TABLE IF NOT EXISTS bot.user_journey
(
    id UUID,
    log_type String,
    time_stamp  DateTime('Europe/Moscow'),
    user_id UInt64,
    app_ver String,
    event_group String,
    event_name String,
    event_data String
)
ENGINE = MergeTree()
PRIMARY KEY (id)
;

CREATE TABLE IF NOT EXISTS bot.errors
(
    id UUID,
    log_type String,
    time_stamp  DateTime('Europe/Moscow'),
    user_id UInt64,
    app_ver String,
    meta_info String,
    reason String,
    category String
)
ENGINE = MergeTree()
PRIMARY KEY (id)
;