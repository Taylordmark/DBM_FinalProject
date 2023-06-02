import sqlite3
import pandas as pd
import random
from pathlib import Path

# Dictionary to map CSV column names to table column names
column_mapping = {
    'Meals': 'title',
    'Need a side?': 'sideRequired',
    'Need a sauce?': 'sauceRequired',
    'Dish Type': 'dishType',
    'Prep Time': 'prepTime',
    'Main Ingredient': 'primaryIngredient',
    'Addtional Ingredients': 'allIngredients',
    'Directions': 'directions',
    'Creator': 'creator'  # Mapping for the 'Creator' column
}

# Function to generate a random creator ID by selecting a random user ID from the User table
def generate_creator_id(num_users):
    return random.randint(1, num_users)

def insert_recipe_data(csv_file, num_users, database_location='activity_recommendations.db'):
    # Connect to the database
    with sqlite3.connect(database_location) as conn:
        cursor = conn.cursor()

        # Clear the Recipe table
        cursor.execute('DELETE FROM Recipe')

        # Read the CSV file using pandas
        df = pd.read_csv(csv_file)

        # Get the column names from the CSV file
        csv_column_names = df.columns.tolist()

        # Map the CSV column names to the table column names
        table_column_names = [column_mapping.get(csv_column_name, csv_column_name) for csv_column_name in csv_column_names]

        # Iterate over each row and insert into the Recipe table
        for index, row in df.iterrows():
            # Check if the title is not null
            if pd.notnull(row['Meals']):
                # Create a dynamic list of values for the columns in the table
                values = [row[csv_column_name] for csv_column_name in csv_column_names]
                creator_id = generate_creator_id(num_users)  # Generate a random creator ID

                # Append the creator ID to the values list
                values.append(creator_id)

                # Generate placeholders for the SQL query
                placeholders = ', '.join(['?'] * (len(csv_column_names) + 1))

                # Prepare the column names for the SQL query
                column_names_sql = ', '.join(['`' + table_column_name + '`' for table_column_name in table_column_names + ['creator']])

                # Execute the SQL query
                cursor.execute(f'''
                    INSERT INTO Recipe ({column_names_sql})
                    VALUES ({placeholders})
                ''', values)


# Example usage
if __name__ == '__main__':
    csv_file_path = str(Path('db_make_files/Recipes.csv'))
    num_users = 5000  # Replace with the actual number of users
    insert_recipe_data(csv_file_path, num_users)
