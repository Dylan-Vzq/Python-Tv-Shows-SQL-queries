# Name: Guillermo L. Rivera Matos
# Student ID: Y00632412

#============================================================================================#
# Using Python with Databases                                                                #
# This Python script serves as a module to connect to MariaDB and perform global             #
# data cleaning to avoid repeating code when information is extracted from the database      #
#============================================================================================#

import mariadb
from mariadb import Error, Connection
import pandas as pd

# Module to connect to MariaDB and perform global data cleaning

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "coen2220",
    "password": "coen2220",
    "database": "group01",
    "port": 3306
}

# Method that connects to MariaDB, loads selected columns, and performs a global cleaning using pandas
def filtered_data():

    # Declare connection variable
    connection: Connection = None

    # Try to perform this block of code
    try:

        # Establish connection to the MariaDB database using the credentials defined in DB_CONFIG
        connection = mariadb.connect(**DB_CONFIG)

        # Load only these columns from the table
        query = ("SELECT name, genres, original_language, vote_average, first_air_date,"
                 " number_of_episodes FROM group01");

        # Read data into a pandas DataFrame
        df = pd.read_sql(query, connection)

        # Remove all the duplicated data
        df = df.drop_duplicates()

        # Remove rows with NULL values in the selected columns that will be loaded
        df = df[
            df["name"].notnull() & df["original_language"].notnull() & df["vote_average"].notnull() &
            df["genres"].notnull() & df["first_air_date"].notnull() & df["number_of_episodes"].notnull()
        ]

        # Convert to datetime and filter by date to avoid erroneous, old or future data
        df["first_air_date"] = pd.to_datetime(df["first_air_date"], errors = "coerce")

        # Filter the data to only include the TV shows released from 1960 onward
        df = df[(df["first_air_date"] >= "1960-01-01") & (df["first_air_date"] <= "2025-11-01")]

        # Create the global "Year" column based on the filter made above for grouping
        df["Year"] = df["first_air_date"].dt.year

        # Display this message if the data was successfully filtered
        print("Data successfully filtered and cleaned. \n")

        return df

    # If an error occurs while connecting to MariaDB, display a message indicating it
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return pd.DataFrame()

    # After loading all data from the Database, always close the connection
    finally:
        if connection:
            connection.close()
            print("Database connection closed.\n")
