#!/usr/bin/env python3
import json
import os

import bottle
import datadog
import pcc
import psycopg2
import psycopg2.extras
from attrdict import AttrDict as attrdict
from first import first

datadog.initialize()
stats = datadog.ThreadStats(["app:comments"])
stats.start()

CONFIG_POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

print("Open database at {}".format(CONFIG_POSTGRES_HOST))
dbpool = pcc.RefreshingConnectionCache(
        lifetime=600,
        host=CONFIG_POSTGRES_HOST, database="postgres",
        user="postgres", password="password",
        cursor_factory=psycopg2.extras.DictCursor)


def is_app_user_agent(user_agent):
    return "okhttp" in user_agent or "pr0gramm-app" in user_agent

def stopwatch_plugin(func):
    def wrapper(*args, **kwargs):
        name = "pr0gramm.kfav.%s" % func.__name__
        user_agent = bottle.request.headers.get("user-agent", "").lower()
        platform = "app" if is_app_user_agent(user_agent) else "browser"
        with stats.timer(name, tags=["platform:%s" % platform]):
            return func(*args, **kwargs)

    return wrapper


bottle.install(stopwatch_plugin)


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

    with dbpool.tx() as database, database.cursor() as cursor:
        # get flag from the database.
        if "flags" not in body:
            cursor.execute('SELECT flags FROM items WHERE id=%s', [body.item_id])
            body.flags = first(row for row, in cursor.fetchall())

        cursor.execute('''
            INSERT INTO comment_favorites (fav_owner, id, item_id, name, content, created, up, down, mark, thumb, flags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (fav_owner, id)
                DO UPDATE SET created=%s, up=%s, down=%s, mark=%s
        ''', [user,
              body.id, body.item_id,
              body.name, body.content, body.created, body.up, body.down, body.mark, body.thumb, body.flags,
              body.created, body.up, body.down, body.mark])


@bottle.get("/<user>")
def list_comments(user):
    flags = int(bottle.request.query.get("flags", 7))
    flags = [flags & f for f in (1, 2, 4)]

    with dbpool.tx() as database, database.cursor() as cursor:
        cursor.execute(
                'SELECT id, item_id, name, content, created, up, down, mark, thumb, flags FROM comment_favorites '
                'WHERE fav_owner=%s AND flags IN %s ORDER BY created DESC',
                [user, tuple(flags)])

        comments = [dict(row) for row in cursor]

    bottle.response.content_type = "application/json"
    return json.dumps(comments)


@bottle.delete("/<user>/<comment_id:int>")
@bottle.post("/<user>/<comment_id:int>/delete")
def delete_comment(user, comment_id):
    with dbpool.tx() as database, database.cursor() as cursor:
        cursor.execute('DELETE FROM comment_favorites WHERE fav_owner=%s AND id=%s',
                       [user, comment_id])


@bottle.route('/<:re:.*>', method='OPTIONS')
def cors_generic_route():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'


def main():
    bottle.run(debug=True, reloader=True)


if __name__ == '__main__':
    main()
