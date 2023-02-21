from flask import request
from flask_restful import Resource
from connection import connection
from psycopg2.extras import RealDictCursor
from errors import CommentNotFoundError, MalformedCommentPatchError

class Comment(Resource):
    def patch(self, comment_id):
        with connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                patch_data = request.get_json()

                # Handle 400s
                if ("body" not in patch_data):
                    raise MalformedCommentPatchError
                
                cursor.execute("""
                  UPDATE comments
                  SET body = (%s), updated_at = NOW()
                  WHERE comment_id = (%s)
                  RETURNING *
                """, (patch_data["body"], comment_id))

                comment = cursor.fetchone()
                if (comment is None):
                    raise CommentNotFoundError
                
                return {"comment": comment}