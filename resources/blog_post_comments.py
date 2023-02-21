from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from psycopg2.errors import InvalidTextRepresentation
from errors import BlogPostNotFoundError, MalformedCommentsPostError, CommentNotFoundError


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

    def post(self, blog_post_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                try:
                    post_data = request.get_json()

                    # Handle 400s
                    if ("body" not in post_data or "user_id" not in post_data):
                        raise MalformedCommentsPostError

                    cursor.execute("""
                    SELECT * FROM blog_posts
                    WHERE blog_post_id = (%s)
                    """, (blog_post_id,))
                    if (cursor.fetchone() is None):
                        raise BlogPostNotFoundError

                    # 404 on no parent comment
                    if (post_data["parent_comment_id"] is not None):
                        cursor.execute("""
                        SELECT * FROM comments
                        WHERE comment_id = (%s)
                        """, (post_data["parent_comment_id"],))
                        if (cursor.fetchone() is None):
                            raise CommentNotFoundError

                    cursor.execute("""
                      INSERT INTO comments (body, parent_comment_id, user_id, blog_post_id)
                      VALUES (%s, %s, %s, %s)
                      RETURNING *
                    """, (post_data["body"], post_data["parent_comment_id"], post_data["user_id"], blog_post_id))

                except InvalidTextRepresentation:
                    raise MalformedCommentsPostError

                return {"comment": cursor.fetchone()}, 201
