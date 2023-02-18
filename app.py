from flask import Flask

app = Flask(__name__)

@app.get("/")
def home():
    return { "data": "Hello world!"}