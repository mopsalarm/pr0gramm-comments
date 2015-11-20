
DROP TABLE IF EXISTS comment_favorites;

CREATE TABLE comment_favorites (
    fav_owner VARCHAR (32) DEFAULT NULL,

    id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    name VARCHAR (255) NOT NULL,
    content TEXT NOT NULL,
    created INTEGER NOT NULL,
    up  INTEGER NOT NULl CHECK (up >= 0),
    down INTEGER NOT NULL CHECK (down >= 0),
    mark INTEGER NOT NULL CHECK (mark >= 0 AND mark < 16)
);

CREATE UNIQUE INDEX "comment_favorites__fav_owner__id" ON comment_favorites(fav_owner, id);
