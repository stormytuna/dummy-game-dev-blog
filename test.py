from app import app

import unittest


class ContentNotFound(unittest.TestCase):
    # 404s on a random endpoint
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/totally-a-real-endpoint")
        status_code = response.status_code
        self.assertEqual(status_code, 404)


class GetPosts(unittest.TestCase):
    # Responds with a 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/")
        self.assertEqual(response.status_code, 200)

    # Content returned is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/")
        self.assertEqual(response.content_type, "application/json")

    # Data returned is an array of blog post objects
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/api/posts/")
        self.assertTrue(b"blog_posts" in response.data)


if __name__ == "__main__":
    unittest.main()
