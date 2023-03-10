from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from psycopg2.errors import InvalidTextRepresentation
from errors import BlogPostNotFoundError, MalformedVotesError


class BlogPostVotes(Resource):
    def patch(self, blog_post_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                patch_data = request.get_json()

                # Handle 400s
                if ("vote_increment" not in patch_data):
                    raise MalformedVotesError

                try:
                    cursor.execute("""
                      UPDATE blog_posts
                      SET votes = votes + (%s)
                      WHERE blog_post_id = (%s)
                      RETURNING *
                    """, (patch_data["vote_increment"], blog_post_id))
                except InvalidTextRepresentation:
                    raise MalformedVotesError

                blog_post = cursor.fetchone()
                if (blog_post is None):
                    raise BlogPostNotFoundError

                return {"blog_post": blog_post}
