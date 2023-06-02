import random
import sqlite3
import string

# Function to generate random x and y coordinates within the US
def generate_coordinates():
    x = round(random.uniform(-125.0, -67.0), 6)
    y = round(random.uniform(24.396308, 49.384358), 6)
    return x, y

# Function to generate random activity titles
def generate_title():
    activities = ['Skiing', 'Hiking', 'Escape Room', 'Cycling', 'Kayaking', 'Rock Climbing', 'Surfing', 'Cooking Class',
                  'Painting Workshop', 'Yoga Session', 'Movie Theater', 'Sightseeing Tour', 'Wine Tasting', 'Photography Walk',
                  'Bowling', 'Go Karting', 'Museum Visit', 'Concert', 'Pottery Making', 'Scuba Diving']
    return random.choice(activities)

# Function to generate a random creator ID by selecting a random user ID from the User table
def generate_creator_id(num_users):
    return random.randint(1, num_users)

# Function to insert activity data into the Activity table
def insert_activity_data(num_activities, num_users, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Get the maximum existing ID in the Activity table
        cursor.execute('SELECT MAX(ID) FROM Activity')
        result = cursor.fetchone()
        max_id = result[0] if result[0] else 0

        # Generate and insert activity data
        for i in range(num_activities):
            activity_id = max_id + i + 1
            coordinates_x, coordinates_y = generate_coordinates()
            title = generate_title()
            creator_id = generate_creator_id(num_users)

            # Execute the SQL query
            cursor.execute('''
                INSERT INTO Activity (ID, coordinates_x, coordinates_y, title, creator)
                VALUES (?, ?, ?, ?, ?)
            ''', (activity_id, coordinates_x, coordinates_y, title, creator_id))

        # Commit the changes (not necessary here since the connection is opened in a with statement)
        # conn.commit()

# Example usage
if __name__ == '__main__':
    num_activities = 50
    insert_activity_data(num_activities)
