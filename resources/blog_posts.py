from flask import request, abort
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from psycopg2.errors import ForeignKeyViolation, InvalidTextRepresentation
from errors import MalformedBlogPostError, UserNotFoundError


class BlogPosts(Resource):
    def get(self):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                  SELECT blog_posts.*, users.username, COUNT(comments.comment_id) as comment_count FROM blog_posts
                  INNER JOIN users ON blog_posts.user_id = users.user_id
                  LEFT JOIN comments ON comments.blog_post_id = blog_posts.blog_post_id
                  GROUP BY blog_posts.blog_post_id, users.username
                """)

                return {"blog_posts": cursor.fetchall()}
            
    def post(self):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                blog_post = request.get_json()

                # Handle 400s
                if ("user_id" not in blog_post or "body" not in blog_post):
                    raise MalformedBlogPostError
                
                try:
                    cursor.execute("""
                      INSERT INTO blog_posts (user_id, body)
                      VALUES (%s, %s)
                      RETURNING *
                    """, (blog_post["user_id"], blog_post["body"]))  
                except ForeignKeyViolation:
                    raise UserNotFoundError
                except InvalidTextRepresentation:
                    raise MalformedBlogPostError
                    

                return {"blog_post": cursor.fetchone()}, 201
