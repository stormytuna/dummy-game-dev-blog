from app import app
from db.seed import seed

import unittest


class ContentNotFound(unittest.TestCase):
    # 404s on a random endpoint
    def test(self):
        tester = app.test_client(self)
        response = tester.get("/totally-a-real-endpoint")
        status_code = response.status_code
        self.assertEqual(status_code, 404)


class GetPosts(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_posts" in response.data)


class GetPost(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_post" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/5000/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)


class GetUsersPosts(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.get("/api/users/1/posts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_posts" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.get("/api/users/5000/posts/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)


class PostPost(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/", json={"user_id": 1, "body": "Grahhhh"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_post" in response.data)

    def test_404_on_user_id(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/", json={"user_id": 5000, "body": "Grahhhh"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_malformed_body(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/", json={"vihsiu": 5000, "afkhfk": "Grahhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_fails_schema_validation(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/", json={"user_id": "not-a-number", "body": "Grahhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()


class PatchBlogPostVotes(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/1/votes/", json={"vote_increment": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_post" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/5000/votes/", json={"vote_increment": 1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_malformed_body(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/1/votes/", json={"vjnsdifijsnis": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_fails_schema_validation(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/1/votes/", json={"vote_increment": "grahh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()


class PatchBlogPost(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/1/", json={"body": "Grahhhhhhh"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_post" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/5000/", json={"body": "Grahhhhhhh"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_malformed_body(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/posts/1/", json={"vjnsdifijsnis": "Grahhhhhhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()


class DeleteBlogPost(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.delete(
            "/api/posts/1/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, "application/json")

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.delete(
            "/api/posts/5000/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()


class GetBlogPostComments(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.get(
            "/api/posts/1/comments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"comments" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.get(
            "/api/posts/5000/comments/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)


class PostComment(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/1/comments/", json={"body": "Grahhhh", "user_id": 1, "parent_comment_id": None})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"comment" in response.data)

    def test_404_on_blog_post_id(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/5000/comments/", json={"body": "Grahhhh", "user_id": 1, "parent_comment_id": None})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_404_on_parent_comment_id(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/1/comments/", json={"body": "Grahhhh", "user_id": 1, "parent_comment_id": 5000})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_malformed_body(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/1/comments/", json={"bsfacadcva": "Grahhhh", "fsgtdehgfsfdgh": 1, "sdgfsdfvsgssg": None})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_fails_schema_validation(self):
        tester = app.test_client(self)
        response = tester.post(
            "/api/posts/1/comments/", json={"body": "Grahhhh", "user_id": "vuiagcuy", "parent_comment_id": "gnaicnaiu"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"comments" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()




class PatchCommentVotes(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/1/votes/", json={"vote_increment": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"comment" in response.data)

    def test_404_on_comment_id(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/5000/votes/", json={"vote_increment": 1})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)  

    def test_400_on_malformed_body(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/5000/votes/", json={"eifhwijhfijdj": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)  

    def test_400_on_fails_schema_validation(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/5000/votes/", json={"vote_increment": "grahhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)  

    def tearDown(self) -> None:
        seed()
        return super().tearDown()
    

class PatchComment(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/1/", json={"body": "Grahhhhhh"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"comment" in response.data)

    def test_404_on_comment_id(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/5000/", json={"body": "Grahhhhhh"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_on_malformed_body(self):
        tester = app.test_client(self)
        response = tester.patch(
            "/api/comments/1/", json={"cnfdijbwiufwi": "Grahhhhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def tearDown(self) -> None:
        seed()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
