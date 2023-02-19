from werkzeug.exceptions import HTTPException

class BlogPostNotFoundError(HTTPException):
    pass

class UserNotFoundError(HTTPException):
    pass