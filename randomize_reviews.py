import random
import sqlite3
import string
import time

# Function to generate a random review text
def generate_review_text(class_name, rating):
    if class_name == 'Recipe':
        if rating <= 2:
            return "I would not recommend this recipe."
        elif rating <= 3:
            return "It was an average recipe."
        elif rating <= 4:
            return "This recipe was good, but could be improved."
        else:
            return "This recipe was fantastic!"
    elif class_name == 'Activity':
        if rating <= 2:
            return "I had a bad experience with this activity."
        elif rating <= 3:
            return "It was an okay activity."
        elif rating <= 4:
            return "I enjoyed this activity."
        else:
            return "This activity was amazing!"

# Function to generate a random review for a specific item
def generate_review_with_delay(item_id, class_name, user_id, database_location='activity_recommendations.db'):
    # Connect to the database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Get the class-specific table name
    table_name = class_name.lower()

    # Get the maximum compositeID in the Review table
    cursor.execute('SELECT MAX(compositeID) FROM Review')
    result = cursor.fetchone()
    max_composite_id = result[0] if result[0] else 0

    # Generate random rating and review text
    rating = random.randint(0, 5)
    review_text = generate_review_text(class_name, rating)

    # Execute the SQL query
    cursor.execute(f'''
        INSERT INTO Review (compositeID, User, itemID, class, ratingValue, ratingText)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (max_composite_id + 1, user_id, item_id, class_name, rating, review_text))

    # Commit the changes
    conn.commit()

    # Close the connection after a delay
    time.sleep(0.1)
    conn.close()

# Function to get a random item ID from the specified table
def get_random_item_id(table_name, database_location='activity_recommendations.db'):
    # Connect to the database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Get the maximum ID from the specified table
    cursor.execute(f'SELECT MAX(ID) FROM {table_name}')
    result = cursor.fetchone()
    max_id = result[0] if result[0] else 0

    # Generate a random item ID
    item_id = random.randint(1, max_id)

    # Close the connection
    conn.close()

    return item_id

# Function to get a random user ID from the User table
def get_random_user_id(database_location='activity_recommendations.db'):
    # Connect to the database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Count the number of rows in the User table
    cursor.execute('SELECT COUNT(*) FROM User')
    result = cursor.fetchone()
    total_users = result[0] if result[0] else 0

    # Generate a random offset to select a random row
    offset = random.randint(0, total_users - 1)

    # Retrieve a random user ID
    cursor.execute(f'SELECT ID FROM User LIMIT 1 OFFSET {offset}')
    result = cursor.fetchone()
    user_id = result[0] if result else None

    # Close the connection
    conn.close()

    return user_id



# Function to generate random reviews
def generate_random_reviews_with_delays(num_reviews, database_location='activity_recommendations.db'):
    # Connect to the database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Clear the Review table
    cursor.execute('DELETE FROM Review')

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Generate random reviews with delays
    for _ in range(num_reviews):
        # Generate random class (Recipe or Activity)
        class_name = random.choice(['Recipe', 'Activity'])

        # Get a random item ID from the corresponding table
        item_id = get_random_item_id(class_name.lower())

        # Get a random user ID
        user_id = get_random_user_id()

        # Generate and insert the review with a delay
        generate_review_with_delay(item_id, class_name, user_id)

if __name__ == '__main__':
    num_reviews = 50
    generate_random_reviews_with_delays(num_reviews)