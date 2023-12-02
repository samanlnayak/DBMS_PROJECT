import streamlit as st
import pymysql
import pandas as pd
import warnings

# Create a connection to the MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1739@Manohar",
    database="TheaterManagement"
)

session_state = st.session_state
privileges = session_state.get('privileges')

# Create a Streamlit app
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

# Set the Streamlit option
st.set_option('deprecation.showfileUploaderEncoding', False)
st.title("Theatre  - Manage")

aggregate_query = """
SELECT
    m.title AS MovieTitle,
    s.start_time AS Showtime,
    t.seat_number AS SeatNumber,
    c.first_name AS CustomerFirstName,
    c.last_name AS CustomerLastName,
    t.price AS TicketPrice
FROM
    Ticket t
JOIN
    Showtime s ON t.showtime_id = s.showtime_id
JOIN
    Movie m ON s.movie_id = m.movie_id
JOIN
    Customers c ON t.customer_id = c.customer_id
ORDER BY
    s.start_time;

"""
nested_query = f"""
           SELECT
    m.title AS MovieTitle,
    s.start_time AS Showtime,
    IFNULL(
        (
            SELECT
                SUM(t.price)
            FROM
                Ticket t
            WHERE
                t.showtime_id = s.showtime_id
        ),
        0
    ) AS TotalRevenue
FROM
    Showtime s
JOIN
    Movie m ON s.movie_id = m.movie_id
WHERE
    m.title <> 'RRR'
ORDER BY
    s.start_time;
        """

def check_login(username, password):
    # Query the database for the user
    query = "SELECT UserID, Privileges FROM User WHERE Username = %s AND Password = %s"
    cursor = connection.cursor()
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        user_id, privileges = result
        st.success("Login successful!")
        # Store the user ID and privileges in the session
        st.session_state['user_id'] = user_id
        st.session_state['privileges'] = privileges
        return True
    else:
        st.error("Invalid username or password.")
        return False
    
def register_user(username, password, privileges):
    # Insert the user into the database
    try:
        # Call the stored procedure to insert the user with admin privileges
        cursor = connection.cursor()
        query = "INSERT INTO User (Username, Password, Privileges) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, privileges))
        connection.commit()
        cursor.close()
        st.success("User registered successfully.")
    except pymysql.Error as err:
        st.error(f"Error: {err}")
        st.error("User registration failed.")

# Function to execute SQL queries and fetch data as a Pandas DataFrame
def execute_query(query, data=None, fetch=True):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        if fetch and cursor.description is not None:
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        connection.rollback()
        return pd.DataFrame()
    


nested_query = """
SELECT
    m.title AS MovieTitle,
    s.start_time AS Showtime,
    (
        SELECT
            SUM(t.price)
        FROM
            Ticket t
        WHERE
            t.showtime_id = s.showtime_id
    ) AS TotalRevenue
FROM
    Showtime s
JOIN
    Movie m ON s.movie_id = m.movie_id
ORDER BY
    s.start_time;
"""

def execute_nested_query():
    st.subheader("Show Gross")
    
    # Execute the nested query
    nested_result = execute_query(nested_query)
    
    # Display the result in a table
    st.table(nested_result)

def display_entity(table_name):
    # Display table
    data = execute_query(f"SELECT * FROM {table_name}")
    st.table(data)

# Function to display and manage entities
def insert_entity(entity_name, table_name, columns):
    st.subheader(entity_name)

    if(privileges=="admin"):
    # Add entry
        st.subheader(f"Add a {entity_name} Entry")
        values = []
        for col_name, col_type in columns:
            if col_type == "int":
                values.append(st.number_input(f"{col_name}"))
            else:
                values.append(st.text_input(f"{col_name}"))
        
        if st.button(f"Add {entity_name}"):
            if all(values):
                query = f"INSERT INTO {table_name} ({', '.join([col[0] for col in columns])}) VALUES ({', '.join(['%s' for _ in columns])})"
                data = tuple(values)
                execute_query(query, data)
                st.success(f"{entity_name} added successfully!")
            else:
                st.error("Please fill in all fields.")
    else:
        st.error("User with standard privileges cannot insert data.")

def update_entity(entity_name, table_name, columns,primary_key):
    if(privileges=="admin"):
        st.subheader(f"Update a {entity_name} Entry")
        id_to_update = st.text_input(f"{primary_key} to update")
        if id_to_update:
            entry_to_update = execute_query(f"SELECT * FROM {table_name} WHERE {primary_key} = %s", (id_to_update,))
            if not entry_to_update.empty:
                update_values = []
                for col_name, col_type in columns:
                    if col_type == "int":
                        update_values.append(st.number_input(f"{col_name}", value=entry_to_update.iloc[0][col_name]))
                    else:
                        update_values.append(st.text_input(f"{col_name}", value=entry_to_update.iloc[0][col_name]))
                if st.button(f"Update {entity_name}"):
                    set_clause = ', '.join([f'{col_name} = %s' for col_name, _ in columns])
                    query = f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s"
                    data = tuple([update_values[i] for i in range(len(columns))] + [id_to_update])
                    execute_query(query, data)
                    st.success(f"{entity_name} updated successfully!")

            else:
                st.error(f"{entity_name} ID not found.")
    else:
        st.error("User with standard privileges cannot update data.")

def delete_entity(entity_name, table_name, columns,primary_key):
    if(privileges=="admin"):
        st.subheader(f"Delete a {entity_name} Entry")
        id_to_delete = st.text_input(f"{primary_key} to delete")
        if id_to_delete:
            if st.button(f"Delete {entity_name}"):
                execute_query(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (id_to_delete,))
                st.success(f"{entity_name} deleted successfully!")
    else:
        st.error("User with standard privileges cannot delete data.")



def join_tables(table1,table2,common_attribute):
    st.subheader("Join Tables")

    if st.button("Perform Join"):
        if table1 != table2:
            join_query = f"""
                SELECT *
                FROM {table1}
                NATURAL JOIN {table2}
            """
            join_result = execute_query(join_query)
            st.table(join_result)
        else:
            st.error("Cannot join the same table. Please select different tables.")

def display_all_users():
    st.subheader("All Users")
    query = "SELECT * FROM User"
    users = execute_query(query, fetch=True)
    st.table(users)

# Function to execute the stored procedure
def execute_get_movie_information(movie_id):
    if st.button('Get Movie Information'):
        cursor = connection.cursor()
        cursor.callproc("GetMovieInformation", [int(movie_id)])
        result = cursor.fetchall()

        if result:
            movie_info = result[0]
            st.write(f"Movie ID: {movie_info[0]}")
            st.write(f"Title: {movie_info[1]}")
            st.write(f"Release Date: {movie_info[2]}")
            st.write(f"Genre: {movie_info[3]}")
            st.write(f"Duration: {movie_info[4]}")
            st.write(f"Theater ID: {movie_info[5]}")
            st.write(f"Description: {movie_info[6]}")
        else:
            st.write("No movie found with the given ID.")


# Streamlit UI


# Define entity information
entity_info = [
    ("Customers", "Customers", [
        ("customer_id", "int"),
        ("first_name", "varchar(50)"),
        ("last_name", "varchar(50)"),
        ("email", "varchar(100)"),
        ("phone", "varchar(20)")
    ]),
    ("Theater", "Theater", [
        ("theater_id", "int"),
        ("name", "varchar(100)"),
        ("location", "varchar(255)"),
        ("capacity", "int")
    ]),
    ("Movie", "Movie", [
        ("movie_id", "int"),
        ("title", "varchar(255)"),
        ("release_date", "date"),
        ("genre", "varchar(50)"),
        ("duration", "int"),
        ("description", "text"),
        ("theater_id", "int")
    ]),
    ("Showtime", "Showtime", [
        ("showtime_id", "int"),
        ("movie_id", "int"),
        ("theater_id", "int"),
        ("start_time", "datetime")
    ]),
    ("Ticket", "Ticket", [
    ("ticket_id", "int"),
    ("showtime_id", "int"),
    ("customer_id", "int"),
    ("seat_number", "varchar(10)"),
    ("price", "decimal(8,2)"),
]),
    ("Employees", "Employee", [
        ("employee_id", "int"),
        ("first_name", "varchar(50)"),
        ("last_name", "varchar(50)"),
        ("position", "varchar(50)"),
        ("theater_id", "int"),
        ("email", "varchar(100)"),
        ("phone", "varchar(20)")
    ]),
    ("TicketCounters", "TicketCounter", [
        ("ticket_counter_id", "int"),
        ("name", "varchar(100)"),
        ("theater_id", "int")
    ]),
    ("User", "User", [
        ("UserID", "int"),
        ("Username", "varchar(50)"),
        ("Password", "varchar(50)"),
        ("Privileges", "enum('admin', 'standard') DEFAULT 'standard'")
    ])
]

is_authenticated = session_state.get('is_authenticated', False)

if not is_authenticated:
    st.title("Theatre -Manage - Register")

    username = st.text_input("Username:", key="username_r")
    password = st.text_input("Password:", key="password_r",type="password")
    privileges = st.selectbox("Select Privileges:", ['admin', 'standard'])

    if st.button("Register"):
        register_user(username, password, privileges)

    # Display the login page
    st.title("Theatre - Manage - Login")

    username = st.text_input("Username:", key="username_l")
    password = st.text_input("Password:", key="password_l", type="password")

    if st.button("Login"):
        if check_login(username, password):
            st.success("Login successful!")
            session_state['is_authenticated'] = True  # Update authentication status
            st.rerun()  # Refresh the page to display the home page
        else:
            st.error("Invalid username or password.")
else:
    # Display the home page
    st.title("Theatre -Manage- Home Page")
    selected_option = st.selectbox("Options", ["Home","Display","Insert", "Update", "Delete","Join","Aggregate-Tickets Sold","Nested-Show Gross","Display Users","Get Movie Information"])

    # Check the selected optio
    if selected_option == "Display":
        selected_entity = st.selectbox("Select a table to view", [entity[0] for entity in entity_info])
        display_entity(selected_entity)

    if selected_option == "Insert":
        selected_entity = st.selectbox("Select an entity to insert", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                insert_entity(entity[0], entity[1], entity[2])

    elif selected_option == "Update":
        selected_entity = st.selectbox("Select an entity to update", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                primary_key = entity[-1][0][0]
                update_entity(entity[0], entity[1], entity[2],primary_key)
                
    elif selected_option == "Delete":
        selected_entity = st.selectbox("Select an entity to delete", [entity[0] for entity in entity_info])
        for entity in entity_info:
            if entity[0] == selected_entity:
                primary_key = entity[-1][0][0]
                delete_entity(entity[0], entity[1], entity[2],primary_key)
    elif selected_option == "Join":
        table1 = st.selectbox("Select first entity to join", [entity[0] for entity in entity_info],key="table1")
        table2 = st.selectbox("Select second entity to join", [entity[0] for entity in entity_info],key="table2")
        common_attribute = st.text_input("Enter the common attribute for the join:")
        join_tables(table1,table2,common_attribute)

    elif selected_option == "Aggregate-Tickets Sold" :
        st.subheader("Tickets Sold")
        total_payment_result = execute_query(aggregate_query)
        st.table(total_payment_result)

    elif selected_option == "Nested-Show Gross" :
        st.subheader("Show  Wise Gross")
        nested_result  = execute_query(nested_query)
        st.table(nested_result )

    elif selected_option == 'Display Users':
        st.header("Users")
        display_all_users()
    elif selected_option == 'Get Movie Information':
        st.header('Get Movie Information')
        movie_id = st.text_input('Enter movie_id')
        execute_get_movie_information(movie_id)
 

# Close the database connection
connection.close()