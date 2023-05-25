import sqlite3
import time

from create_database import create_tables
from fill_activities import insert_activity_data
from fill_recipes import insert_recipe_data
from randomize_users import insert_user_data
from randomize_reviews import generate_random_reviews_with_delays

if __name__ == '__main__':
    
    database_name = ('activity_recommendations.db')
    num_activities = 100
    activities_file = 'Activities.csv'
    recipes_file = 'Recipes.csv'
    review_count = 100
    num_users = 50

    create_tables(database_location=database_name)
    sqlite3.connect('activity_recommendations.db').close()
    insert_user_data(num_users)
    sqlite3.connect('activity_recommendations.db').close()
    insert_activity_data(num_activities, activities_file)
    sqlite3.connect('activity_recommendations.db').close()
    insert_recipe_data(recipes_file)
    sqlite3.connect('activity_recommendations.db').close()
    generate_random_reviews_with_delays(review_count)
    sqlite3.connect('activity_recommendations.db').close()
