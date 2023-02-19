from werkzeug.exceptions import HTTPException


class BlogPostNotFoundError(HTTPException):
    pass


class UserNotFoundError(HTTPException):
    pass


class MalformedBlogPostError(HTTPException):
    pass


class MalformedBlogPostVotesError(HTTPException):
    pass


class MalformedBlogPostPatchError(HTTPException):
    pass
