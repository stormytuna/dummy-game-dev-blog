from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor


class BlogPosts(Resource):
  # TODO: Make this endpoint return username instead of user id and comment count
    def get(self):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM blog_posts;")
                return {"blog_posts": cursor.fetchall()}
