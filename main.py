#!/usr/bin/env python3
import json
import os

import bottle
import psycopg2
import psycopg2.extras
from attrdict import AttrDict as attrdict

CONFIG_POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

print("Open database at {}".format(CONFIG_POSTGRES_HOST))
db = psycopg2.connect(host=CONFIG_POSTGRES_HOST, database="postgres",
                      user="postgres", password="password",
                      cursor_factory=psycopg2.extras.DictCursor)


@bottle.hook('after_request')
def enable_cors():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'


@bottle.post("/<user>")
@bottle.put("/<user>/<comment_id:int>")
def store_comment(user, comment_id=None):
    body = attrdict(bottle.request.json)
    if comment_id and body.id != comment_id:
        raise bottle.abort(400)

    with db, db.cursor() as cursor:
        cursor.execute('''
            INSERT INTO comment_favorites (fav_owner, id, item_id, name, content, created, up, down, mark)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (fav_owner, id)
                DO UPDATE SET created=%s, up=%s, down=%s, mark=%s
        ''', [user,
              body.id, body.item_id,
              body.name, body.content, body.created, body.up, body.down, body.mark,
              body.created, body.up, body.down, body.mark])


@bottle.get("/<user>")
def list_comments(user):
    with db, db.cursor() as cursor:
        cursor.execute(
            'SELECT id, item_id, name, content, created, up, down, mark FROM comment_favorites '
            'WHERE fav_owner=%s ORDER BY created DESC',
            [user])

        comments = [dict(row) for row in cursor]

    bottle.response.content_type = "application/json"
    return json.dumps(comments)


@bottle.delete("/<user>/<comment_id:int>")
@bottle.post("/<user>/<comment_id:int>/delete")
def delete_comment(user, comment_id):
    with db, db.cursor() as cursor:
        cursor.execute('DELETE FROM comment_favorites WHERE fav_owner=%s AND id=%s',
                       [user, comment_id])


def main():
    bottle.run(debug=True, reloader=True)


if __name__ == '__main__':
    main()
