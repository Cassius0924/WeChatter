-- 创建 copilot_chats 表
PRAGMA foreign_keys = false;

CREATE TABLE IF NOT EXISTS "copilot_chats"
(
   chat_id           integer not null
        constraint copilot_chats_pk
            primary key autoincrement,
    wx_id             integer
        constraint copilot_chats_wx_users_wx_id_fk
            references wx_users,
    chat_topic        TEXT,
    chat_created_time TIMESTAMP default CURRENT_TIMESTAMP,
    chat_talk_time    TIMESTAMP,
    chat_model        TEXT,
    is_chating        BLOB      default TRUE
);

PRAGMA foreign_keys = true;
