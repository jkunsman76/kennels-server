import sqlite3
import json
from models.animal import Animal

ANIMALS = [
    {
        "id": 1,
        "name": "Doodles",
        "breed": "German Shepherd",
        "locationId": 1,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "id": 3,
        "name": "Angus",
        "breed": "Dalmatian 👾",
        "locationId": 1,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "id": 4,
        "name": "Henley",
        "breed": "Carolina Retriever 🚒",
        "locationId": 1,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "id": 5,
        "name": "Derkins",
        "breed": "Shih tzu 👿",
        "locationId": 2,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "id": 6,
        "name": "Checkers",
        "breed": "Bulldog",
        "locationId": 1,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "Sawyer",
        "breed": "Lollie",
        "id": 7,
        "locationId": 2,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "Gypsy",
        "breed": "Miniature Schnauzer",
        "id": 8,
        "locationId": 1,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "Zipper",
        "breed": "Terrier",
        "locationId": 2,
        "id": 9,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "Blue",
        "breed": "Hound dog",
        "locationId": 2,
        "id": 10,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "Bugle",
        "breed": "Beagle",
        "locationId": 1,
        "id": 11,
        "status": "Admitted",
        "customerId": 1
    },
    {
        "name": "pohtaytoe",
        "breed": "mutt",
        "employeeId": 3,
        "locationId": None,
        "id": 12,
        "status": "Admitted",
        "customerId": 1
    }
]


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])

            animals.append(animal.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(animals)


# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])

        return json.dumps(animal.__dict__)


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal


def delete_animal(id):
    # Initial -1 value for animal index, in case one isn't found
    animal_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Store the current index.
            animal_index = index

    # If the animal was found, use pop(int) to remove it from list
    if animal_index >= 0:
        ANIMALS.pop(animal_index)


def update_animal(id, new_animal):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Update the value.
            ANIMALS[index] = new_animal
            break
