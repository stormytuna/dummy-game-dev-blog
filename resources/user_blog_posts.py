from flask import abort
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor


class UserBlogPosts(Resource):
    def get(self, user_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # 404 if no user
                cursor.execute("""
                    SELECT * FROM users 
                    WHERE user_id = (%s)
                """, (user_id,))
                user = cursor.fetchone()
                if (user is None):
                    abort(404, f"User with id={user_id} not found")

                cursor.execute("""
                  SELECT blog_posts.*, users.username, COUNT(comments.comment_id) as comment_count FROM blog_posts
                  INNER JOIN users ON blog_posts.user_id = users.user_id
                  LEFT JOIN comments ON comments.blog_post_id = blog_posts.blog_post_id
                  WHERE users.user_id = (%s)
                  GROUP BY blog_posts.blog_post_id, users.username
                """, (user_id,))


                return {"blog_posts": cursor.fetchall()}
