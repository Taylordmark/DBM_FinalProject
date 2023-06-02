from db_transactions import *

import sqlite3

get_user_reviews(30, database_location='activity_recommendations.db')

# get_similar_users(user_id, database_location='activity_recommendations.db')

# correct request types are 'recipe' or 'activity'
# get_recommendations('ayXsvmVE@uiUNy.com', request_type = 'activity')
# user_id = 
# add_new_review(user_id, item_id, class_name, rating, review_text, database_location='activity_recommendations.db')
# add_new_activity(self)
# calculate_average_rating(item_id, class_name, database_location='activity_recommendations.db')