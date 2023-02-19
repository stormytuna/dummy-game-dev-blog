from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from errors import BlogPostNotFoundError, MalformedBlogPostPatchError


class BlogPost(Resource):
    def get(self, blog_post_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                  SELECT blog_posts.*, users.username, COUNT(comments.comment_id) as comment_count FROM blog_posts
                  INNER JOIN users ON blog_posts.user_id = users.user_id
                  LEFT JOIN comments ON comments.blog_post_id = blog_posts.blog_post_id
                  WHERE blog_posts.blog_post_id = (%s)
                  GROUP BY blog_posts.blog_post_id, users.username
                """, (blog_post_id,))

                # Handle 404s
                blog_post = cursor.fetchone()
                if (blog_post is None):
                    raise BlogPostNotFoundError

                return {"blog_post": blog_post}

    def patch(self, blog_post_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                patch_data = request.get_json()

                # Handle 400s
                if ("body" not in patch_data):
                    raise MalformedBlogPostPatchError

                cursor.execute("""
                  UPDATE blog_posts
                  SET body = (%s), updated_at = NOW()
                  WHERE blog_post_id = (%s)
                  RETURNING *
                """, (patch_data["body"], blog_post_id))

                blog_post = cursor.fetchone()
                if (blog_post is None):
                    raise BlogPostNotFoundError

                return {"blog_post": blog_post}
