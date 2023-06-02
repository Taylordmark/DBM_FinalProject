import sqlite3
import time

from db_make_files.create_database import create_tables
from db_make_files.fill_activities import insert_activity_data
from db_make_files.fill_recipes import insert_recipe_data
from db_make_files.randomize_users import insert_user_data
from db_make_files.randomize_reviews import generate_random_reviews_with_delays

if __name__ == '__main__':
    
    database_name = 'activity_recommendations.db'
    num_activities = 10000
    recipes_file = 'db_make_files/Recipes.csv'
    review_count = 10000
    num_users = 5000

    create_tables(database_location=database_name)
    insert_user_data(num_users)
    insert_activity_data(num_activities, num_users)
    insert_recipe_data(recipes_file, num_users)
    generate_random_reviews_with_delays(review_count)
