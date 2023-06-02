from db_transactions import *

import sqlite3

# Pick a user email from the generated DB
email = 'ayXsvmVE@uiUNy.com'

# Get Reviews
# user index can be any value between min and max of User table, but not all will have reviews associated
reviews = get_user_reviews(user_index = 30)
print(reviews)

# Get Similar Users
# Using the same email as before
similar_users = get_similar_users(user_id = email)

# Get User Recommendations
# correct request types are 'recipe' or 'activity'
recommendations = get_recommendations(user_email = email, request_type = 'activity')

# Add New Recipe
# Set recipe values for addition to db
title = 'cookies'
side_required = None
dish_type = 'Dessert'
sauce_required = None
prep_time = 30
primary_ingredient = 'flour'
all_ingredients = 'flour; 3, chocolate chips; 2, baking_powder; 2, eggs; 4'
directions = "Mix the stuff then make cookie shapes and bake"

# Get recipe addition results
success, inputted_value = add_new_recipe(title, side_required, sauce_required, dish_type, prep_time, primary_ingredient, all_ingredients,
                   directions)
print(success, inputted_value)

# Add New Activity
# Set activity values for addition to db
name = 'kayaking'
x_location = 39.8752694
y_location = -85.1233838

# Get activity input value results
success, inputted_value = add_new_activity(name, x_location, y_location, email)
print(success, inputted_value)               

# Add New Review
# Set input values for review addition
# Class name is 'Recipe' or 'Activity'
class_name = 'Recipe'
rating = 4
item_id = 20
review_text = 'This recipe was delicious!'
success, inputted_data = add_new_review(email, item_id, class_name, rating, review_text)
print(success, inputted_data)

# Set item index to get ratings
item_index = 30
class_name = 'Recipe'

average_rating = calculate_average_rating(30, class_name)
print(average_rating)