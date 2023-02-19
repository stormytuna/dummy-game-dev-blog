from flask import Flask
from flask_restful import Api
from resources.blog_posts import BlogPosts
from resources.blog_post import BlogPost
from resources.user_blog_posts import UserBlogPosts
from resources.blog_post_votes import BlogPostVotes
from resources.blog_post_comments import BlogPostComments
from resources.endpoints import Endpoints
from errors import *

app = Flask(__name__)
api = Api(app, errors={
    "BlogPostNotFoundError": {
        "message": "Blog post not found",
        "status": 404
    },
    "UserNotFoundError": {
        "message": "User not found",
        "status": 404
    },
    "MalformedBlogPostError": {
        "message": "Malformed blog post received, ensure your sent request has 'user_id:integer' and 'body:string' properties",
        "status": 400
    },
    "ForeignKeyViolation": {
        "message": "Bad request",
        "status": 400
    },
    "MalformedBlogPostVotesError": {
        "message": "Malformed blog post votes received, ensure your sent request has a 'vote_increment:integer' property",
        "status": 400
    },
    "MalformedBlogPostPatchError": {
        "message": "Malformed blog post patch received, ensure your sent request has a 'body:string' property",
        "status": 400
    }
})

api.add_resource(Endpoints, "/api/")
api.add_resource(BlogPosts, "/api/posts/")
api.add_resource(BlogPost, "/api/posts/<int:blog_post_id>/")
api.add_resource(UserBlogPosts, "/api/users/<int:user_id>/posts/")
api.add_resource(BlogPostVotes, "/api/posts/<int:blog_post_id>/votes/")
api.add_resource(BlogPostComments, "/api/posts/<int:blog_post_id>/comments/")
