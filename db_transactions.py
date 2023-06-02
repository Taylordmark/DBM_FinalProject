import sqlite3
import random

def get_user_reviews(user_index, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Retrieve the user ID based on the user index
        cursor.execute(f'SELECT ID FROM User LIMIT 1 OFFSET {user_index}')
        result = cursor.fetchone()
        user_id = result[0] if result else None

        # Retrieve the reviews for the user
        cursor.execute(f'SELECT * FROM Review WHERE User = ?', (user_id,))
        reviews = cursor.fetchall()

    return reviews

def get_similar_users(user_id, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Retrieve the user's age, interest, and city
        cursor.execute('SELECT Age, classofInterest, cityofResidence FROM User WHERE ID = ?', (user_id,))
        user_info = cursor.fetchone()
        user_age, user_interest, user_city = user_info

        # Retrieve similar users based on age, interest, and city
        cursor.execute('SELECT ID FROM User WHERE Age < ? + 10 AND Age > ? - 10 AND classofInterest = ? AND cityofResidence = ?', 
                       (user_age, user_age, user_interest, user_city))
        similar_users = cursor.fetchall()

    return [user[0] for user in similar_users]

def suggest_activity_or_recipe(user_id, request_type, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Get similar users based on age, interest, and city
        similar_users = get_similar_users(user_id, database_location)

        if request_type == 'activity':
        # Retrieve activities and recipes reviewed by similar users
            cursor.execute('''
            SELECT itemID FROM Review WHERE User IN ({}) AND class = 'Activity'
            '''.format(','.join(['?'] * len(similar_users))), similar_users)
            
            response = cursor.fetchall()

        else:
            cursor.execute('''
            SELECT itemID FROM Review WHERE User IN ({}) AND class = 'Recipe'
            '''.format(','.join(['?'] * len(similar_users))), similar_users)

            response = cursor.fetchall()
        
        random_item = random.choice(response)[0]

        if request_type == 'activity':
            # Get the suggested activity
            cursor.execute('SELECT * FROM Activity WHERE ID = ?', (random_item,))
            response = cursor.fetchone()

        else:
            # Get the suggested recipe
            cursor.execute('SELECT * FROM Recipe WHERE ID = ?', (random_item,))
            response = cursor.fetchone()

        return response

    return None

def get_recommendations(user_email, request_type = 'activity'):
    def get_bool_as_string(self):
        if self == 0:
            self = 'No'
        else:
            self = 'Yes'
        
    user_id = user_email
    response = suggest_activity_or_recipe(user_id, request_type)
    if response:
        if request_type=='activity':
            print("Suggested Activities:")
            print(f"Activity: {response[3]}\nLocation: {response[1],response[2]}\n \n ID: {response[0]}, Creator: {response[4]}\n")
        else:
            print("Suggested Recipes:")
            print(f"ID: {response[0]}, Title: {response[1]}, \n Side: {get_bool_as_string(response[2])}, Sauce: {get_bool_as_string(response[3])}, Dish Type: {response[5]}, Prep Time: {response[6]} \n\n \
                    Primary Ingredient: {response[7]}\n\n\
                    All Ingredients: {response[8]} \n\n\
                    Directions: {response[9]} \n \n \
                    Creator: {response[4]}")
    else:
        print("No suggestions available.")

def create_new_user(email, name, age, city, zipcode, interest, database_location='activity_recommendations.db'):
    """
    Create a new user in the database.

    Args:
        email (str): The email address of the user.
        name (str): The name of the user.
        age (int): The age of the user.
        city (str): The city of residence of the user.
        zipcode (str): The zip code of the user.
        interest (str): The class of interest for the user.
        database_location (str): The path to the SQLite database file.
    """
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to create a new user
        cursor.execute('''
            INSERT INTO User (ID, Name, Age, cityofResidence, zipcode, classofInterest)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, name, age, city, zipcode, interest))

def add_new_review(user_id, item_id, class_name, rating, review_text, database_location='activity_recommendations.db'):
    """
    Add a new review to the Review table in the database.

    Args:
        user_id (str): The ID of the user who wrote the review.
        class_name (str): The class name of the item being reviewed ('Recipe' or 'Activity').
        rating (int): The rating value of the review.
        review_text (str): The text of the review.
        database_location (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing the success status (True or False) and the inputted data.
    """

    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        try:
            # Get the total number of rows in the Review table
            cursor.execute('SELECT COUNT(*) FROM Review')
            total_rows = cursor.fetchone()[0]

            # Increment item_id by 1 based on the total number of rows
            item_id = total_rows + 1

            composite_id = f"{user_id}_{item_id}_{class_name}"

            # Execute the SQL query to add a new review
            cursor.execute('''
                INSERT INTO Review (compositeID, User, itemID, class, ratingValue, ratingText)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (composite_id, user_id, item_id, class_name, rating, review_text))

            # Commit the changes to the database
            conn.commit()

            # Return success status and inputted data
            return True, (user_id, class_name, rating, review_text)

        except sqlite3.Error:
            # Return failure status and inputted data
            return False, (user_id, class_name, rating, review_text)

def add_new_recipe(title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients,
                   directions, database_location='activity_recommendations.db'):
    """
    Add a new recipe to the Recipe table in the database.

    Args:
        title (str): The title of the recipe.
        side_required (str): Indicates if a side is required for the recipe.
        sauce_required (str): Indicates if a sauce is required for the recipe.
        dish_type (str): The type of dish (e.g., appetizer, main course).
        prep_time (int): The preparation time of the recipe in minutes.
        primary_ingredient (str): The primary ingredient of the recipe.
        all_ingredients (str): The list of all ingredients required for the recipe.
        directions (str): The cooking directions for the recipe.
        database_location (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing the success status (True or False) and the inputted data.
    """
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        try:
            # Execute the SQL query to add a new recipe
            cursor.execute('''
                INSERT INTO Recipe (title, sideRequired, sauceRequired, dishType, prepTime, primaryIngredient, allIngredients, directions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients, directions))

            # Commit the changes to the database
            conn.commit()

            # Return success status and inputted data
            return True, (title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients, directions)

        except sqlite3.Error:
            # Return failure status and inputted data
            return False, (title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients, directions)
    
def add_new_activity(title, x_location, y_location, user_email, database_location='activity_recommendations.db'):
    """
    Add a new activity to the Activity table in the database.

    Args:
        title (str): The title of the activity.
        x_location (float): The x-coordinate location of the activity.
        y_location (float): The y-coordinate location of the activity.
        user_email (str): The email of the user associated with the activity.
        database_location (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing the success status (True or False) and the inputted data.
    """
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Get the number of rows in the Activity table
        cursor.execute('SELECT COUNT(*) FROM Activity')
        count = cursor.fetchone()[0]

        # Increment the ID based on the table size
        ID_count = count + 1

        # Find the associated user index based on the email
        cursor.execute('SELECT ROWID FROM User WHERE ID = ?', (user_email,))
        user_index = cursor.fetchone()[0]

        try:
            # Execute the SQL query to add a new activity
            cursor.execute('''
                INSERT INTO Activity (coordinates_x, coordinates_y, title, creator)
                VALUES (?, ?, ?, ?)
            ''', (x_location, y_location, title, user_index))

            # Commit the changes to the database
            conn.commit()

            # Return success status and inputted data
            return True, (x_location, y_location, title, user_index)

        except sqlite3.Error:
            # Return failure status and inputted data
            return False, (x_location, y_location, title, user_index)

def calculate_average_rating(item_id, class_name, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Retrieve the ratings for the specified item
        cursor.execute('SELECT ratingValue FROM Review WHERE itemID = ? AND class = ?', (item_id, class_name))
        ratings = cursor.fetchall()

    # Calculate the average rating
    if ratings:
        total_ratings = len(ratings)
        sum_ratings = sum(rating[0] for rating in ratings)
        average_rating = sum_ratings / total_ratings
        return average_rating

    return 0.0  # Default average rating if no ratings found