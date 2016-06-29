
-- DROP TABLE IF EXISTS comment_favorites;

CREATE TABLE IF NOT EXISTS comment_favorites (
    fav_owner VARCHAR (32) DEFAULT NULL,

    id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    name VARCHAR (255) NOT NULL,
    content TEXT NOT NULL,
    created INTEGER NOT NULL,
    up  INTEGER NOT NULl CHECK (up >= 0),
    down INTEGER NOT NULL CHECK (down >= 0),
    mark INTEGER NOT NULL CHECK (mark >= 0 AND mark < 16),
    thumb VARCHAR (255) NOT NULL,
    flags INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS user_token (
  mail_hash VARCHAR(32) NOT NULL,
  token VARCHAR(32) NOT NULL
);


CREATE UNIQUE INDEX IF NOT EXISTS "comment_favorites__fav_owner__id" ON comment_favorites(fav_owner, id);
CREATE UNIQUE INDEX IF NOT EXISTS "user_token__mail_hash" ON user_token(mail_hash);
