from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from errors import BlogPostNotFoundError


class BlogPostComments(Resource):
    def get(self, blog_post_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check blog post exists
                cursor.execute("""
                  SELECT * FROM blog_posts
                  WHERE blog_post_id = (%s)
                """, (blog_post_id,))

                blog_post = cursor.fetchone()
                if (blog_post is None):
                    raise BlogPostNotFoundError

                cursor.execute("""
                  SELECT comments.*, users.username FROM blog_posts
                  JOIN comments ON blog_posts.blog_post_id = comments.blog_post_id
                  JOIN users ON comments.user_id = users.user_id
                  WHERE blog_posts.blog_post_id = (%s)
                """, (blog_post_id,))

                return {"comments": cursor.fetchall()}
