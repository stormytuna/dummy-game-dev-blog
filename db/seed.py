import os
import psycopg2
import json
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")
seed_data = os.getenv("SEED_DATA")
connection = psycopg2.connect(url)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


def delete_existing_data(cursor):
    cursor.execute("DROP TABLE IF EXISTS blog_posts")
    cursor.execute("DROP TABLE IF EXISTS comments")
    cursor.execute("DROP TABLE IF EXISTS users;")

    cursor.execute("""
      CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(40) NOT NULL,
        joined VARCHAR(100) NOT NULL DEFAULT NOW(),
        last_activity VARCHAR(100) NOT NULL DEFAULT NOW()
      );
    """)
    cursor.execute("""
      CREATE TABLE comments (
        comment_id SERIAL PRIMARY KEY,
        parent_comment_id INTEGER,
        blog_post_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        body VARCHAR(1000) NOT NULL,
        created_at VARCHAR(100) NOT NULL DEFAULT NOW(),
        updated_at VARCHAR(100) NOT NULL DEFAULT NOW(),
        votes INTEGER NOT NULL DEFAULT 0
      )
    """)
    cursor.execute("""
      CREATE TABLE blog_posts (
        blog_post_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users ON DELETE CASCADE,
        body VARCHAR(2000) NOT NULL,
        created_at VARCHAR(100) NOT NULL DEFAULT NOW(),
        updated_at VARCHAR(100) NOT NULL DEFAULT NOW(),
        votes INTEGER NOT NULL DEFAULT 0
      );
    """)


def insert_data(cursor):
    data_path = "./db/data/prod.json" if seed_data == "prod" else "./db/data/test.json"
    with open(data_path) as data:
        data_contents = data.read()

    parsed_data = json.loads(data_contents)

    users_data = parsed_data["users"]
    blog_posts_data = parsed_data["blog_posts"]
    comments_data = parsed_data["comments"]

    # Users
    for user in users_data:
        cursor.execute("""
          INSERT INTO users (username, joined, last_activity) 
          VALUES (%s, %s, %s)
        """, (user["username"], user["joined"], user["last_activity"]))

    # Blog posts
    for blog_post in blog_posts_data:
        cursor.execute("""
        INSERT INTO blog_posts (user_id, body, created_at, updated_at, votes)
        VALUES (%s, %s, %s, %s, %s)
      """, (blog_post["user_id"], blog_post["body"], blog_post["created_at"], blog_post["updated_at"], blog_post["votes"]))

    # Comments
    for comment in comments_data:
        cursor.execute("""
        INSERT INTO comments (parent_comment_id, blog_post_id, user_id, body, created_at, updated_at, votes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
      """, (comment["parent_comment_id"], comment["blog_post_id"], comment["user_id"], comment["body"], comment["created_at"], comment["updated_at"], comment["votes"]))


def seed():
    with connection:
        with connection.cursor() as cursor:
            delete_existing_data(cursor)
            insert_data(cursor)


def main():
    seed()
    connection.close()


if __name__ == "__main__":
    main()
