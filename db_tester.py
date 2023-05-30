import sqlite3
import unittest

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Connect to the database
        self.conn = sqlite3.connect('activity_recommendations.db')
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def test_user_table_exists(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='User'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_recipe_table_exists(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Recipe'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_activity_table_exists(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Activity'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_review_table_exists(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Review'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_insert_user(self):
        self.cursor.execute("INSERT INTO User (ID, Name, Age, cityofResidence, zipcode, classofInterest) "
                            "VALUES ('testuser', 'John Doe', 25, 'City', 12345, 'Cooking')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM User WHERE ID='testuser'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_insert_recipe(self):
        self.cursor.execute("INSERT INTO Recipe (ID, title, sideRequired, sauceRequired, creator, dishType, "
                            "prepTime, primaryIngredient, allIngredients, directions) "
                            "VALUES (1, 'Pasta Carbonara', 1, 0, 'testuser', 'Main Course', 30, 'Pasta', "
                            "'Pasta, Eggs, Bacon, Parmesan Cheese', 'Cook the pasta...')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Recipe WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_insert_activity(self):
        self.cursor.execute("INSERT INTO Activity (ID, coordinates_x, coordinates_y, title, creator) "
                            "VALUES (1, 0.0, 0.0, 'Hiking', 'testuser')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Activity WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_insert_review(self):
        self.cursor.execute("INSERT INTO Review (compositeID, User, itemID, class, ratingValue, ratingText) "
                            "VALUES ('review1', 'testuser', 1, 'Recipe', 4.5, 'Delicious dish')")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Review WHERE compositeID='review1'")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)

    def test_delete_user(self):
        self.cursor.execute("DELETE FROM User WHERE ID='testuser'")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM User WHERE ID='testuser'")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_recipe(self):
        self.cursor.execute("DELETE FROM Recipe WHERE ID=1")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Recipe WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_activity(self):
        self.cursor.execute("DELETE FROM Activity WHERE ID=1")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Activity WHERE ID=1")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_delete_review(self):
        self.cursor.execute("DELETE FROM Review WHERE compositeID='review1'")
        self.conn.commit()

        self.cursor.execute("SELECT * FROM Review WHERE compositeID='review1'")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
