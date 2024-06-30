import pandas as pd
import sqlite3
from sqlalchemy import create_engine


# Expanded exercise data
exercise_data = {
    'day': ['Pull Day', 'Push Day', 'Leg Day', 'Rest Day', 'Full Body Day', 'Cardio Day'],
    'exercises': [
        [
            {'exercise_name': 'Pull-Up', 'sets': 4, 'reps': 8, 'description': 'Wide grip pull-ups'},
            {'exercise_name': 'Deadlift', 'sets': 3, 'reps': 6, 'description': 'Standard deadlifts'},
            {'exercise_name': 'Bicep Curl', 'sets': 3, 'reps': 10, 'description': 'Using dumbbells'},
            {'exercise_name': 'Rowing Machine', 'sets': 4, 'reps': 200, 'description': '200 meters per set'}
        ],
        [
            {'exercise_name': 'Bench Press', 'sets': 4, 'reps': 8, 'description': 'Flat bench press'},
            {'exercise_name': 'Overhead Press', 'sets': 3, 'reps': 6, 'description': 'Using barbell'},
            {'exercise_name': 'Tricep Dip', 'sets': 3, 'reps': 10, 'description': 'Bodyweight or weighted'},
            {'exercise_name': 'Chest Fly', 'sets': 3, 'reps': 12, 'description': 'Using cables'}
        ],
        [
            {'exercise_name': 'Squat', 'sets': 4, 'reps': 8, 'description': 'Barbell back squat'},
            {'exercise_name': 'Leg Press', 'sets': 3, 'reps': 10, 'description': 'Machine leg press'},
            {'exercise_name': 'Calf Raise', 'sets': 3, 'reps': 15, 'description': 'Standing calf raises'},
            {'exercise_name': 'Lunges', 'sets': 3, 'reps': 12, 'description': 'Dumbbell lunges'}
        ],
        [
            {'exercise_name': 'Burpees', 'sets': 3, 'reps': 15, 'description': 'High intensity'},
            {'exercise_name': 'Mountain Climbers', 'sets': 4, 'reps': 20, 'description': 'High intensity'},
            {'exercise_name': 'Jump Squats', 'sets': 3, 'reps': 12, 'description': 'Bodyweight'},
            {'exercise_name': 'Push-Ups', 'sets': 4, 'reps': 20, 'description': 'Bodyweight'}
        ],
        [
            {'exercise_name': 'Running', 'sets': 1, 'reps': 30, 'description': '30 minutes on treadmill'},
            {'exercise_name': 'Cycling', 'sets': 1, 'reps': 30, 'description': '30 minutes on stationary bike'},
            {'exercise_name': 'Elliptical', 'sets': 1, 'reps': 30, 'description': '30 minutes on elliptical'},
            {'exercise_name': 'Stair Climber', 'sets': 1, 'reps': 20, 'description': '20 minutes on stair climber'}
        ]
    ]
}

# Expanded nutrition data
nutrition_data = {
    'meal': ['Breakfast', 'Lunch', 'Dinner', 'Snack', 'Pre-Workout', 'Post-Workout', 'Midnight Snack'],
    'food_items': [
        ['Oatmeal', 'Banana', 'Almonds', 'Coffee'],
        ['Grilled Chicken', 'Brown Rice', 'Broccoli', 'Salad'],
        ['Salmon', 'Quinoa', 'Asparagus', 'Sweet Potato'],
        ['Greek Yogurt', 'Blueberries', 'Honey', 'Nuts'],
        ['Protein Shake', 'Banana', 'Peanut Butter'],
        ['Chicken Breast', 'Sweet Potato', 'Green Beans'],
        ['Cottage Cheese', 'Almonds', 'Apple']
    ],
    'nutrition_details': [
        {'calories': 400, 'protein': 18, 'carbs': 50, 'fats': 12},
        {'calories': 600, 'protein': 45, 'carbs': 60, 'fats': 15},
        {'calories': 650, 'protein': 50, 'carbs': 65, 'fats': 20},
        {'calories': 300, 'protein': 12, 'carbs': 30, 'fats': 10},
        {'calories': 350, 'protein': 25, 'carbs': 40, 'fats': 8},
        {'calories': 500, 'protein': 40, 'carbs': 50, 'fats': 12},
        {'calories': 250, 'protein': 15, 'carbs': 20, 'fats': 8}
    ]
}

# Convert to DataFrames
exercise_df = pd.DataFrame(exercise_data)
nutrition_df = pd.DataFrame(nutrition_data)


# Function to create SQLite database and tables
def create_sqlite_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create exercise table
    cursor.execute('''
    CREATE TABLE exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT,
        exercise_name TEXT,
        sets INTEGER,
        reps INTEGER,
        description TEXT
    )
    ''')

    # Create nutrition table
    cursor.execute('''
    CREATE TABLE nutrition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meal TEXT,
        food_items TEXT,
        calories INTEGER,
        protein INTEGER,
        carbs INTEGER,
        fats INTEGER
    )
    ''')

    conn.commit()
    conn.close()

# Function to insert data into SQLite database
def insert_data_into_database(df, table_name, db_name):
    engine = create_engine(f'sqlite:///{db_name}')
    df.to_sql(table_name, con=engine, if_exists='append', index=False)


# Example function to insert exercise data with vector
def insert_exercises_into_database(exercise_df, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for index, row in exercise_df.iterrows():
        day = row['day']
        for exercise in row['exercises']:
            exercise_name = exercise['exercise_name']
            sets = exercise['sets']
            reps = exercise['reps']
            description = exercise['description']

            cursor.execute('''
            INSERT INTO exercises (day, exercise_name, sets, reps, description)
            VALUES (?, ?, ?, ?, ?)
            ''', (day, exercise_name, sets, reps, description))
    conn.commit()
    conn.close()

# Example function to insert nutrition data with vector
def insert_nutrition_into_database(nutrition_df, db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for index, row in nutrition_df.iterrows():
        meal = row['meal']
        food_items = ', '.join(row['food_items'])
        calories = row['nutrition_details']['calories']
        protein = row['nutrition_details']['protein']
        carbs = row['nutrition_details']['carbs']
        fats = row['nutrition_details']['fats']

        cursor.execute('''
        INSERT INTO nutrition (meal, food_items, calories, protein, carbs, fats)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (meal, food_items, calories, protein, carbs, fats))
    conn.commit()
    conn.close()

# Create SQLite database and tables
db_name = 'fitness_data.db'
create_sqlite_database(db_name)

# Insert exercise and nutrition data into SQLite database
insert_exercises_into_database(exercise_df, db_name)
insert_nutrition_into_database(nutrition_df, db_name)

print(f"Database '{db_name}' created and populated with exercise and nutrition data.")
