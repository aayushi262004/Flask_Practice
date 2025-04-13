import unittest
from main import create_app
from config import TestConfig
from exts import db


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client(self)

        with self.app.app_context():
            db.create_all()

    def test_hello_world(self):
        hello_response = self.client.get('/recipe/hello')
        json = hello_response.json
        self.assertEqual(json, {"message": "Hello World"})

    def test_signup(self):
        signup_response = self.client.post(
            '/auth/signup',
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password"
            }
        )
        self.assertEqual(signup_response.status_code, 201)

    def test_login(self):
        self.client.post(
            '/auth/signup',
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password"
            }
        )

        login_response = self.client.post(
            '/auth/login',
            json={
                "username": "testuser",
                "password": "password"
            }
        )
        self.assertEqual(login_response.status_code, 200)

    def test_get_all_recipes(self):
        response = self.client.get('/recipe/recipes')
        self.assertEqual(response.status_code, 200)

    def test_get_one_recipe(self):
        response = self.client.get('/recipe/recipe/1')
        self.assertEqual(response.status_code, 404)

    def test_create_recipe(self):
        self.client.post(
            '/auth/signup',
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password"
            }
        )

        login_response = self.client.post(
            '/auth/login',
            json={
                "username": "testuser",
                "password": "password"
            }
        )
        access_token = login_response.json["access_token"]

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            json={
                "title": "Test Cookie",
                "description": "Test description"
            },
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        self.assertEqual(create_recipe_response.status_code, 201)

        # Test if recipe is retrievable
        recipe_id = create_recipe_response.json["id"]
        get_one = self.client.get(f'/recipe/recipe/{recipe_id}')
        self.assertEqual(get_one.status_code, 200)
        print(get_one.json)

    def test_update_recipe(self):
        self.client.post(
            '/auth/signup',
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password"
            }
        )

        login_response = self.client.post(
            '/auth/login',
            json={
                "username": "testuser",
                "password": "password"
            }
        )
        access_token = login_response.json["access_token"]

        create_response = self.client.post(
            '/recipe/recipes',
            json={
                "title": "Old Title",
                "description": "Old description"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        recipe_id = create_response.json["id"]

        update_response = self.client.put(
            f'/recipe/recipe/{recipe_id}',
            json={
                "title": "Updated Title",
                "description": "Updated description"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["title"], "Updated Title")

    def test_delete_recipe(self):
        self.client.post(
            '/auth/signup',
            json={
                "username": "testuser",
                "email": "testuser@test.com",
                "password": "password"
            }
        )

        login_response = self.client.post(
            '/auth/login',
            json={
                "username": "testuser",
                "password": "password"
            }
        )
        access_token = login_response.json["access_token"]

        create_response = self.client.post(
            '/recipe/recipes',
            json={
                "title": "Recipe to delete",
                "description": "Will be deleted"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )
        recipe_id = create_response.json["id"]

        delete_response = self.client.delete(
            f'/recipe/recipe/{recipe_id}',
            headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(delete_response.status_code, 204)

        # Confirm deletion
        confirm_get = self.client.get(f'/recipe/recipe/{recipe_id}')
        self.assertEqual(confirm_get.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
