-- 创建 chat_conversations 表
PRAGMA foreign_keys = false;

CREATE TABLE IF NOT EXISTS "chat_conversations"
(
    conversation_id        INTEGER not null
        constraint chat_conversations_pk
            primary key autoincrement,
    chat_id                INTEGER
        constraint chat_conversations_copilot_chats_chat_id_fk
            references copilot_chats,
    conversation_timestamp TIMESTAMP,
    conversation_role      TEXT,
    conversation_content   TEXT,
    constraint conversation_role_check
        check ("chat_conversations".conversation_role IN ('system', 'user', 'assistant'))
);

PRAGMA foreign_keys = true;

