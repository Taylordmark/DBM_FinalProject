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
        cursor.execute('SELECT ID FROM User WHERE Age < ? + 10 AND Age > ? - 10 OR classofInterest = ? OR cityofResidence = ?', 
                       (user_age, user_age, user_interest, user_city))
        similar_users = cursor.fetchall()

    return [user[0] for user in similar_users]

def suggest_activity_and_recipe(user_id, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Get similar users based on age, interest, and city
        similar_users = get_similar_users(user_id, database_location)

        # Retrieve activities and recipes reviewed by similar users
        cursor.execute('''
        SELECT itemID FROM Review WHERE User IN ({})
        '''.format(','.join(['?'] * len(similar_users))), similar_users)
        
        reviewed_items = cursor.fetchall()

        # If no reviews found, retrieve items from Activity table
        if not reviewed_items:
            cursor.execute('''
            SELECT ID FROM Activity WHERE User IN ({})
            '''.format(','.join(['?'] * len(similar_users))), similar_users)

            reviewed_items = cursor.fetchall()

        # Randomly suggest an activity and recipe from the reviewed items
        if reviewed_items:
            random_item = random.choice(reviewed_items)[0]

            # Get the suggested activity
            cursor.execute('SELECT * FROM Activity WHERE ID = ?', (random_item,))
            suggested_activity = cursor.fetchone()

            # Get the suggested recipe
            cursor.execute('SELECT * FROM Recipe WHERE ID = ?', (random_item,))
            suggested_recipe = cursor.fetchone()

            return suggested_activity, suggested_recipe

    return None, None

def get_recommendations(user_email):
    def get_bool_as_string(self):
        if self == 0:
            self = 'No'
        else:
            self = 'Yes'
        
    user_id = user_email
    suggested_activity, suggested_recipe = suggest_activity_and_recipe(user_id)
    if suggested_activity or suggested_recipe:
        if suggested_activity:
            print("Suggested Activities:")
            active = suggested_activity
            print(f"Activity: {active[3]}\nLocation: {active[1],active[2]}\n \n ID: {active[0]}, Creator: {active[4]}\n")
        if suggested_recipe:
            print("Suggested Recipes:")
            r = suggested_recipe 
            print(f"ID: {r[0]}, Title: {r[1]}, \n Side: {get_bool_as_string(r[2])}, Sauce: {get_bool_as_string(r[3])}, Dish Type: {r[5]}, Prep Time: {r[6]} \n\n \
                    Primary Ingredient: {r[7]}\n\n\
                    All Ingredients: {r[8]} \n\n\
                    Directions: {r[9]} \n \n \
                    Creator: {r[4]}")

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
        composite_id (str): The composite ID of the review.
        user_id (str): The ID of the user who wrote the review.
        item_id (int): The ID of the item (recipe or activity) being reviewed.
        class_name (str): The class name of the item being reviewed ('Recipe' or 'Activity').
        rating (int): The rating value of the review.
        review_text (str): The text of the review.
        database_location (str): The path to the SQLite database file.
    """

    composite_id = f"{user_id}_{item_id}_{class_name}"
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to add a new review
        cursor.execute('''
            INSERT INTO Review (compositeID, User, itemID, class, ratingValue, ratingText)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, item_id, class_name, rating, review_text))

def add_new_recipe(self):
    title = self.recipe_title_entry.get()
    side_required = self.side_required_entry.get()
    sauce_required = self.sauce_required_entry.get()
    dish_type = self.dish_type_entry.get()
    prep_time = int(self.prep_time_entry.get())
    primary_ingredient = self.primary_ingredient_entry.get()
    all_ingredients = self.all_ingredients_entry.get()
    directions = self.directions_entry.get()

    # Call the add_new_recipe function with the provided inputs
    add_new_recipe(title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients,
                   directions)

    messagebox.showinfo('Success', 'New recipe added successfully.')

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
    """
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to add a new recipe
        cursor.execute('''
            INSERT INTO Recipe (title, sideRequired, sauceRequired, dishType, prepTime, primaryIngredient, allIngredients, directions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients, directions))

        # No need to commit changes since the connection is opened in a with statement

def add_new_activity(self):
    name = self.activity_name_entry.get()
    category = self.activity_category_entry.get()
    location = self.activity_location_entry.get()
    duration = int(self.activity_duration_entry.get())
    description = self.activity_description_entry.get()

    # Call the add_new_activity function with the provided inputs
    add_new_activity(name, category, location, duration, description)

    messagebox.showinfo('Success', 'New activity added successfully.')

    """
    Add a new activity to the Activity table in the database.

    Args:
        name (str): The name of the activity.
        category (str): The category of the activity.
        location (str): The location of the activity.
        duration (int): The duration of the activity in minutes.
        description (str): The description of the activity.
        database_location (str): The path to the SQLite database file.
    """
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Execute the SQL query to add a new activity
        cursor.execute('''
            INSERT INTO Activity (name, category, location, duration, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, category, location, duration, description))

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