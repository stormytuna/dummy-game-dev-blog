from flask import Flask
from flask_restful import Api
from resources.blog_posts import BlogPosts


app = Flask(__name__)
api = Api(app)

api.add_resource(BlogPosts, "/api/posts/")
