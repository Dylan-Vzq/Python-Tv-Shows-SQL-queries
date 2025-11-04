#system file and directory operations (such as to check if the group member files exist)
import os
#access for Python environment (to run group member's scripts with my Python environment[which has all the packages, libs, & the interpreter)
import sys
#runs other scripts (to run the group member's script)
import subprocess
import mariadb
import pandas as pd
import matplotlib.pyplot as plt
from mariadb import Error
import seaborn as sns

#visuals
sns.set_style('whitegrid')
sns.set_palette('deep')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'coen2220',
    'password': 'coen2220',
    'database': 'group01',
    'port': 3306,
}
#count genres each show has (commas indicate 1 more so +1), then calculate the average rating per amount of genre
SQL_QUERY_Q1 = """
SELECT 
    LENGTH(genres) - LENGTH(REPLACE(genres, ',', '')) + 1 AS num_genres,
    AVG(vote_average) AS avg_rating
FROM tvshows
WHERE genres IS NOT NULL AND vote_average IS NOT NULL
GROUP BY num_genres
ORDER BY num_genres;
"""

#group the shows by # of seasons, then calculate average rating per show group
SQL_QUERY_Q2 = """
SELECT 
    CASE 
        WHEN number_of_seasons > 50 THEN '50+'
        ELSE CAST(number_of_seasons AS CHAR)
    END AS num_seasons,
    AVG(vote_average) AS avg_rating
FROM tvshows
WHERE number_of_seasons IS NOT NULL AND vote_average IS NOT NULL
GROUP BY num_seasons
ORDER BY num_seasons+0;
"""

#extract release year from the column of the date, then calculate average rating per year
SQL_QUERY_Q3 = """
SELECT 
    YEAR(first_air_date) AS release_year,
    AVG(vote_average) AS avg_rating
FROM tvshows
WHERE first_air_date IS NOT NULL AND vote_average IS NOT NULL
GROUP BY release_year
HAVING release_year <= 2025
ORDER BY release_year;
"""

#Mention top 20 shows with the highest amount of episodes
SQL_QUERY_Q4 = """
SELECT 
    name,
    number_of_episodes
FROM tvshows
WHERE number_of_episodes IS NOT NULL
ORDER BY number_of_episodes DESC
LIMIT 20;
"""

#grouping shows into ranges (popularity groups)
SQL_QUERY_Q5 = """
SELECT 
    CASE
        WHEN vote_count < 100 THEN '0–99'
        WHEN vote_count < 500 THEN '100–499'
        WHEN vote_count < 1000 THEN '500–999'
        WHEN vote_count < 5000 THEN '1k–4.9k'
        ELSE '5k+'
    END AS vote_range,
    AVG(vote_average) AS avg_rating
FROM tvshows
WHERE vote_average IS NOT NULL
GROUP BY vote_range
ORDER BY 
    CASE vote_range
        WHEN '0–99' THEN 1
        WHEN '100–499' THEN 2
        WHEN '500–999' THEN 3
        WHEN '1k–4.9k' THEN 4
        WHEN '5k+' THEN 5
    END;
"""

def dylan_question1():
    #1. Do shows with more genres tend to have higher ratings?
    #read its respective query
    connection = mariadb.connect(**DB_CONFIG)
    q1 = pd.read_sql_query(SQL_QUERY_Q1, connection)
    connection.close()

    #graph
    plt.figure(figsize=(10,6))
    sns.barplot(data=q1, x="num_genres", y="avg_rating", color= "#3E92CC", edgecolor="black", label= "average rating")
    plt.title("Average Rating compared with Number of Genres in Shows")
    plt.xlabel("Number of genres")
    plt.ylabel("Average Rating")
    plt.tight_layout()
    plt.show()

def dylan_question2():
    #2. How does the average rating vary depending on the number of seasons a show has?
    #read its respective query
    connection = mariadb.connect(**DB_CONFIG)
    q2 = pd.read_sql_query(SQL_QUERY_Q2, connection)
    connection.close()

    #graph
    plt.figure(figsize=(10,6))
    sns.barplot(data=q2, x="num_seasons", y="avg_rating", edgecolor="black", label= "average rating")
    plt.title("Average Rating compared with Number of Seasons in Shows")
    plt.xlabel("Number of Seasons")
    plt.ylabel("Average Rating")
    plt.legend()
    plt.tight_layout()
    plt.show()

def dylan_question3():
    #3. What is the trend of average ratings by release year?
    #read its respective query
    connection = mariadb.connect(**DB_CONFIG)
    q3 = pd.read_sql_query(SQL_QUERY_Q3, connection)
    connection.close()

    #graph
    plt.figure(figsize=(11,6))
    sns.lineplot(data=q3, x="release_year", y="avg_rating", color="#9B5DE5", linewidth=1.5, label= "average rating")
    plt.title("Trend of Average Ratings by Release Year")
    plt.xlabel("Year")
    plt.ylabel("Average Rating")
    plt.grid(True, linestyle="--", alpha=0.5);
    plt.legend()
    plt.tight_layout()
    plt.show()

def dylan_question4():
    #4. Which shows have the highest number of episodes?
    #read its respective query
    connection = mariadb.connect(**DB_CONFIG)
    q4 = pd.read_sql_query(SQL_QUERY_Q4, connection)
    connection.close()

    #graph
    plt.figure(figsize=(11,8))
    q4 = q4.sort_values("number_of_episodes", ascending=True)
    sns.barplot(data=q4, x="number_of_episodes", y="name", orient="h", edgecolor="black", label= "episodes")
    plt.title("Top 20 Shows with the highest number of episodes")
    plt.xlabel("Number of Episodes")
    plt.ylabel("Show")
    plt.tight_layout()
    plt.show()

def dylan_question5():
    #5. How does the average rating vary by vote popularity (grouped by vote count)?
    #read its respective query
    connection = mariadb.connect(**DB_CONFIG)
    q5 = pd.read_sql_query(SQL_QUERY_Q5, connection)
    connection.close()

    #graph
    plt.figure(figsize=(10,6))
    sns.barplot(data=q5, x="vote_range", y="avg_rating", color="#E63946", edgecolor="black", label= "average rating")
    plt.title("Average rating by vote popularity (Grouped by Vote Count)")
    plt.xlabel("Vote Count range")
    plt.ylabel("Average Rating")
    plt.legend()
    plt.tight_layout()
    plt.show()

def dylan_graphs_run():
    #runs my graphs
    dylan_question1()
    dylan_question2()
    dylan_question3()
    dylan_question4()
    dylan_question5()

#run another group member script & then return to the menu so the user can choose another group member
def run_groupMember_script(script):
    #makes sure the group member script runs on my python interpreter in order to avoid version conflicts and also doesn't matter whether you moved your project from (CMD, VSCode, etc) it runs
    py = sys.executable
    if not os.path.exists(script):
        print("Error in run_groupMember_script, not found")
        return
    try:
        #this is to return to the menu after closing the graphs
        subprocess.run([py, script], check=False)
    except Exception as e:
        print(f"Error in run_groupMember_script, not running: {e}")

def menu():
    while True:
        print("\n" + "="*50)
        print(" Select a group member to show his graphs: ")
        print(" 1) Dylan Vazquez Claudio")
        print(" 2) Guillermo Rivera Matos")
        print(" 3) Sergio Sanchez Torrado")
        print(" 4) Quit")
        print("="*72)
        #Makes input regardless if user type a space after or before selection and regardless user types it lowercase or uppercase
        choice = input("Enter selection: ").strip().lower()

        if choice == "1":
            dylan_graphs_run()
        elif choice == "2":
            run_groupMember_script("graph.py")
        elif choice == "3":
            run_groupMember_script("tvdb.py")
        elif choice == "4":
            print("See ya!")
            break
        else:
            print("Invalid")

#run the visualization
if __name__ == "__main__":
    menu()


