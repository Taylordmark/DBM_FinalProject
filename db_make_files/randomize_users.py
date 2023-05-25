import random
import string
import sqlite3

# Function to generate a random email
def generate_email():
    letters = string.ascii_letters
    username = ''.join(random.choice(letters) for _ in range(8))
    domain = ''.join(random.choice(letters) for _ in range(5))
    extension = random.choice(['com', 'net', 'org'])
    return f"{username}@{domain}.{extension}"

# Function to generate random names
def generate_name():
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'William', 'Olivia', 'James', 'Emma', 'Benjamin', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Anderson', 'Thomas', 'Martinez', 'Jones', 'Garcia', 'Davis']
    return random.choice(first_names) + ' ' + random.choice(last_names)

# Function to generate random ages between 18 and 65
def generate_age():
    return random.randint(18, 65)

# Function to generate random cities of residence
def generate_city():
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
              'Dallas', 'San Jose']
    return random.choice(cities)

# Function to generate random zip codes
def generate_zipcode():
    return random.randint(10000, 99999)

# Function to generate random class of interest
def generate_class_of_interest():
    classes = ['thrills', 'adventure', 'arts', 'eccentrics', 'fitness', 'music', 'technology', 'science', 'sports', 'nature']
    return random.choice(classes)

# Function to insert user data into the User table
def insert_user_data(num_users, database_location='activity_recommendations.db'):
    # Connect to the database
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()

    # Clear the User table
    cursor.execute('DELETE FROM User')

    # Generate and insert user data
    for _ in range(num_users):
        email = generate_email()
        name = generate_name()
        age = generate_age()
        city = generate_city()
        zipcode = generate_zipcode()
        class_of_interest = generate_class_of_interest()

        # Execute the SQL query
        cursor.execute('''
            INSERT INTO User (ID, Name, Age, cityofResidence, zipcode, classofInterest)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, name, age, city, zipcode, class_of_interest))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Example usage
if __name__ == '__main__':
    num_users = 50
    insert_user_data(num_users)
