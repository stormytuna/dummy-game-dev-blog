from flask import Flask
from flask_restful import Api
from resources.blog_posts import BlogPosts
from resources.blog_post import BlogPost

app = Flask(__name__)
api = Api(app)

api.add_resource(BlogPosts, "/api/posts/")
api.add_resource(BlogPost, "/api/posts/<int:blog_post_id>/")
