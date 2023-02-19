from app import app

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

    def test_404(self):
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

    def test_404(self):
        tester = app.test_client(self)
        response = tester.get("/api/users/5000/posts/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

class PostPost(unittest.TestCase):
    def test_successful(self):
        tester = app.test_client(self)
        response = tester.post("/api/posts/", json={"user_id": 1, "body": "Grahhhh"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"blog_post" in response.data)

    def test_404(self):
        tester = app.test_client(self)
        response = tester.post("/api/posts/", json={"user_id": 5000, "body": "Grahhhh"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_Malformed_Body(self):
        tester = app.test_client(self)
        response = tester.post("/api/posts/", json={"vihsiu": 5000, "afkhfk": "Grahhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)

    def test_400_Fails_Schema_Validation(self):
        tester = app.test_client(self)
        response = tester.post("/api/posts/", json={"user_id": "not-a-number", "body": "Grahhhh"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"message" in response.data)


if __name__ == "__main__":
    unittest.main()
