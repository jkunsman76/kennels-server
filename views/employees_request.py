import sqlite3
import json
from models.employee import Employee
from models.location import Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jessica Younker",
        "email": "jessica@younker.com",
        "employee": True
    },
    {
        "id": 2,
        "name": "Jordan Nelson",
        "email": "jordan@nelson.com",
        "employee": True
    },
    {
        "id": 3,
        "name": "Zoe LeBlanc",
        "email": "zoe@leblanc.com",
        "employee": True
    },
    {
        "name": "Meg Ducharme",
        "email": "meg@ducharme.com",
        "id": 4,
        "employee": True
    },
    {
        "name": "Hannah Hall",
        "email": "hannah@hall.com",
        "id": 5,
        "employee": True
    },
    {
        "name": "Emily Lemmon",
        "email": "emily@lemmon.com",
        "id": 6,
        "employee": True
    },
    {
        "name": "Jordan Castelloe",
        "email": "jordan@castelloe.com",
        "id": 7,
        "employee": True
    },
    {
        "name": "Leah Gwin",
        "email": "leah@gwin.com",
        "id": 8,
        "employee": True
    },
    {
        "name": "Caitlin Stein",
        "email": "caitlin@stein.com",
        "id": 9,
        "employee": True
    },
    {
        "name": "Greg Korte",
        "email": "greg@korte.com",
        "id": 10,
        "employee": True
    },
    {
        "name": "Charisse Lambert",
        "email": "charisse@lambert.com",
        "id": 11,
        "employee": True
    },
    {
        "name": "Madi Peper",
        "email": "madi@peper.com",
        "id": 12,
        "employee": True
    },
    {
        "name": "Jenna Solis",
        "email": "jenna@solis.com",
        "id": 14,
        "employee": True
    },
    {
        "name": "Eric \"Macho Man\" Taylor",
        "email": "macho@man.com",
        "employee": True,
        "id": 22
    },
    {
        "name": "Jacob R Kunsman",
        "employee": True,
        "email": "jkoonman@gmail.com",
        "id": 23
    },

]


def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM employee e
        JOIN Location l
            ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class above.
            employee = Employee(row['id'], row['name'],
                            row['address'], row['location_id'])
            location = Location(row['id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                            data['location_id'])

        return json.dumps(employee.__dict__)


def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            (
            name,
            address,
            location_id )
        VALUES
            ( ?, ?, ?);
        """, (new_employee['name'], new_employee['address'],
                 new_employee['location_id'],))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the employee dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


    return json.dumps(new_employee)


def delete_employee(id):
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    # Iterate the EMPLOYEES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break

def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'],
                            row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)