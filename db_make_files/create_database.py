import sqlite3
import os

def create_tables(database_location='activity_recommendations.db'):
    # Delete the database file if it exists
    if os.path.exists(database_location):
        os.remove(database_location)
        print(f"Deleted existing database file: {database_location}")

    # Connect to the database (or create it if it doesn't exist)
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Create the User table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                ID VARCHAR PRIMARY KEY,
                Name TEXT,
                Age INTEGER,
                cityofResidence TEXT,
                zipcode INTEGER,
                classofInterest TEXT
            )
        ''')

        # Create index on User table
        cursor.execute('CREATE INDEX idx_user_id ON User (ID)')

        # Create the Recipe table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipe (
                ID INTEGER PRIMARY KEY,
                title TEXT,
                sideRequired BOOLEAN,
                sauceRequired BOOLEAN,
                creator INTEGER,
                dishType TEXT,
                prepTime INTEGER,
                primaryIngredient TEXT,
                allIngredients TEXT,
                directions TEXT,
                FOREIGN KEY (creator) REFERENCES User(ID)
            )
        ''')

        # Create the Activity table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Activity (
                ID INTEGER PRIMARY KEY,
                coordinates_x REAL,
                coordinates_y REAL,
                title TEXT,
                creator INTEGER,
                FOREIGN KEY (creator) REFERENCES User(ID)
            )
        ''')

        # Create the Review table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Review (
                compositeID TEXT PRIMARY KEY,
                User INTEGER,
                itemID INTEGER,
                class TEXT,
                ratingValue REAL,
                ratingText TEXT,
                FOREIGN KEY (User) REFERENCES User(ID),
                FOREIGN KEY (itemID) REFERENCES Recipe(ID) ON DELETE CASCADE,
                FOREIGN KEY (itemID) REFERENCES Activity(ID) ON DELETE CASCADE
            )
        ''')

        # Create index on Review table
        cursor.execute('CREATE INDEX idx_review_user ON Review (User)')

if __name__ == '__main__':
    create_tables()
