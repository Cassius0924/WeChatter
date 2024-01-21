-- 创建 wx_users 表
PRAGMA foreign_keys = false;

CREATE TABLE IF NOT EXISTS "wx_users"
(
    wx_id     TEXT not null
        constraint wx_users_pk
            primary key,
    wx_name   TEXT,
    wx_alias  TEXT,
    wx_gender TEXT,
    constraint gender_check
        check ("wx_users".wx_gender in ('male', 'female', 'unknown'))
);

PRAGMA foreign_keys = true;
