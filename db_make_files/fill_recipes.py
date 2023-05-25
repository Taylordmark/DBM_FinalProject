import sqlite3
import pandas as pd

# Dictionary to map CSV column names to table column names
column_mapping = {
    'Meals': 'title',
    'Need a side?': 'sideRequired',
    'Need a sauce?': 'sauceRequired',
    'Dish Type': 'dishType',
    'Prep Time': 'prepTime',
    'Main Ingredient': 'primaryIngredient',
    'Addtional Ingredients': 'allIngredients',
    'Directions': 'directions'
}

def insert_recipe_data(csv_file, database_location='activity_recommendations.db'):
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

                # Generate placeholders for the SQL query
                placeholders = ', '.join(['?'] * len(csv_column_names))

                # Prepare the column names for the SQL query
                column_names_sql = ', '.join(['`' + table_column_name + '`' for table_column_name in table_column_names])

                # Execute the SQL query
                cursor.execute(f'''
                    INSERT INTO Recipe ({column_names_sql})
                    VALUES ({placeholders})
                ''', values)

        # Commit the changes (not necessary here since the connection is opened in a with statement)
        # conn.commit()

# Example usage
if __name__ == '__main__':
    csv_file_path = 'Recipes.csv'
    insert_recipe_data(csv_file_path)
