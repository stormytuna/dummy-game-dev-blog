from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from psycopg2.errors import InvalidTextRepresentation
from errors import CommentNotFoundError, MalformedVotesError

class CommentVotes(Resource):
    def patch(self, comment_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                patch_data = request.get_json()

                # Handle 400s
                if ("vote_increment" not in patch_data):
                    raise MalformedVotesError
                
                try:
                    cursor.execute("""
                      UPDATE comments
                      SET votes = votes + (%s)
                      WHERE comment_id = (%s)
                      RETURNING *
                    """, (patch_data["vote_increment"], comment_id))
                except InvalidTextRepresentation:
                    raise MalformedVotesError
                
                comment = cursor.fetchone()
                if (comment is None):
                    raise CommentNotFoundError
                
                return {"comment": comment}