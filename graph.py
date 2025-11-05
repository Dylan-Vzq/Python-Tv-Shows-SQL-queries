# Name: Guillermo L. Rivera Matos
# Student ID: Y00632412

#==========================================================================================#
# Using Python Databases Project                                                           #
# This Python script details the individual analysis followed to answer five queries       #
# using a dataset to retrieve information and display it using graphs using libraries      #
#==========================================================================================#

from data_filtered import filtered_data # Import the filtered DataFrame module
import matplotlib.pyplot as plt # Import the matplot library to generate graph plots
import warnings # Import the warnings library to ignore a message when running the program

# First Query: Which years within the 2010s decade saw the highest surge in TV show production?

# Method to develop the full query procedure
def tv_shows_per_year():

    # Load the filtered data from the external module
    df = filtered_data()

    # Keep only data from 2010 to 2020
    df = df[(df["Year"]>=2010) & (df["Year"]<=2020)]

    # Count how many shows there are per year using the globally created column Year and convert the result in DataFrame
    grouped = df["Year"].value_counts().reset_index(name= "Total TV Shows")

    # Sort ascending by year
    grouped = grouped.sort_values(by="Year", ascending=True)

    # Display a title
    print("\nTV Show Production per Year (2010-2020)\n")

    # Display results in the console terminal, and set the default index to not appear
    print(grouped.to_string(index=False))


    # Style the visualization of the graph

    # Establish a figure size
    plt.figure(figsize = (10,8))

    # Title style
    plt.title("TV Show Production During the 2010s", fontsize=22,family="Arial", fontweight="bold", color="#004D7A")

    # Set plot line graph, and customize the color and width of the line
    plt.plot(grouped["Year"], grouped["Total TV Shows"], linewidth=2.5, color = "#1CD7B8", marker = "o",
             label = "TV Shows Released per Year")

    # Customize the style for the x-axis label
    plt.xlabel("Year", fontsize=20, family="Arial", fontweight="bold", color="#7C6A0A")

    # Customize the style for the y-axis label style too
    plt.ylabel("Number of Shows", fontsize=20, family="Arial", fontweight="bold", color="#7C6A0A")

    # Increase the size of the ticks (numbers) in both axis
    plt.tick_params(axis="x", labelsize=14)
    plt.tick_params(axis="y", labelsize=14)

    # Show all year labels in the x-axis
    plt.xticks(grouped["Year"], rotation=45)

    # Present a visible grid in the graph
    plt.grid(True, linestyle='--', linewidth=0.8, color="#B0B0B0", alpha=1)

    # Add a small legend
    plt.legend(fontsize=14)

    # Allows the axis labels to be displayed correctly
    plt.tight_layout()

    # Display the graph
    plt.show()




# Second Query: What percentage of all TV shows belong to each language?

# Method to develop the full query procedure
def language_percentage():

    # Load the filtered data from the external module
    df = filtered_data()

    # Keep only  column for this query's purposes
    df = df[["original_language"]]

    # Define top 10 list of the most common languages
    main_languages = ["en", "zh", "ja", "ko", "de", "fr", "es", "pt", "ru", "it"]

    # Create a new column that keeps the languages that are on the top 10 list, and group as "Others" the languages
    # that are not in the list
    df["language_group"] = df["original_language"].where(df["original_language"].isin(main_languages), "Others")

    # Count total shows per language group
    grouped = df["language_group"].value_counts().reset_index(name="Total TV Shows")

    # Sort the values in descending order
    grouped = grouped.sort_values(by="Total TV Shows", ascending=False)

    # Calculate the percentage that represents each language
    grouped["Percentage"] = (grouped["Total TV Shows"] / grouped["Total TV Shows"].sum()) * 100

    # Language dictionary to replace language codes with the complete language name
    language_names = {
        "en": "English", "zh": "Chinese", "ja" : "Japanese", "ko" : "Korean" , "de": "German", "fr": "French",
        "es": "Spanish", "pt": "Portuguese", "ru": "Russian","it": "Italian", "Others": "Other Languages"
    }

    # Replace properly each language code with its language name
    grouped["Language Name"] = grouped["language_group"].map(language_names)

    # Display a title
    print("\nPercentage of TV Shows by Original Language\n")

    # Display results using the proper columns from the DataFrame
    print(grouped[["Language Name", "Total TV Shows", "Percentage"]].to_string(index=False))


    # Style the visualization of the graph

    # Adjust the size of the figure
    plt.figure(figsize = (13,9))

    # Add a title to the pie chart
    plt.title("Percentage of TV Shows by Original Language", fontsize=20, fontweight="bold", color="#004D7A")

    # Unique color list for each language using the color picker
    colors = ["#0077B6", "#00B4D8", "#F94144", "#7CF820", "#90BE6D", "#FFFF1A",
              "#50FF8A", "#FF6F61", "#7963AA", "#FF1493", "#FF8800"]

    # Create a pie chart to express the results accordingly and customize it using these arguments
    plt.pie(grouped["Percentage"], autopct="%1.1f%%", startangle=180,
            textprops={"fontsize": 14, "color": "#000000"}, colors=colors,
            wedgeprops ={"edgecolor":"#000000","linewidth":1}
    )

    # Add a legend on the right side and adjust it properly
    plt.legend(grouped["Language Name"], title ="Languages", loc ="center left", bbox_to_anchor=(1.07, 0.5),
               fontsize = 14, title_fontsize = 14)

    # Increase separation between labels
    plt.tight_layout()

    # Display pie chart
    plt.show()




# Third Query: Which genres have the highest average rating?

# Method to develop the full query procedure
def avg_rating_by_genre():

    #Load filtered dataset
    df = filtered_data()

    # Keep only the necessary columns
    df = df[["genres", "vote_average", "name"]]

    # If "genres" column has multiple genres per show, separate into individual rows
    df["genres"] = df["genres"].str.split(", ")

    # Each genre in its own row
    df = df.explode("genres")

    # Group by genre and calculate average rating
    grouped = df.groupby("genres")["vote_average"].mean().reset_index(name="Average Rating")

    # Rename column
    grouped = grouped.rename(columns={"genres": "Genres"})

    # Sort descending and keep top 10 genres (exclude the other 10 genres, 20 in total)
    grouped = grouped.sort_values(by="Average Rating", ascending=False).head(10)

    # Add a title
    print("\nTop 10 genres with highest average rating\n")

    # Print results
    print(grouped.to_string(index=False))


    # Style graph visualization

    # Set a figure size
    plt.figure(figsize=(10, 6))

    # Unique color list for each genre using the color picker
    colors = [
        "#0077B6", "#B4D873", "#E7EF1B", "#48CAE4", "#ADE8F4",
        "#F4A300", "#E63946", "#9C27B0", "#00B050", "#6A994E"
    ]

    # Create vertical bars individually with labels to use a bar plot
    bars = plt.bar(grouped["Genres"], grouped["Average Rating"], color=colors)

    # Adjust the y-axis label
    plt.ylabel("Average Rating", fontsize=14, fontweight="bold")
    plt.title("Top 10 Genres with Highest Average Ratings",
              fontsize=18, fontweight="bold", color="#004D7A")

    # Add a legend and adjust it properly
    plt.legend(bars,grouped["Genres"], title="Genres", loc="center left", bbox_to_anchor=(1.07, 0.5), fontsize = 14)

    # Due to a legend being applied, remove the ticks on the x-axis to avoid conflict when visualizing the graph
    plt.xticks([])

    # Increase separation to avoid cuts
    plt.tight_layout()

    # Display graph
    plt.show()



# Forth Query: Which genres have the most long-running shows (over 100 episodes)?

# Method to develop the full query procedure
def genres_with_long_shows():

    # Load filtered data set
    df = filtered_data()

    # Keep only the necessary columns
    df = df[["genres", "number_of_episodes"]]

    # If "genres" column has multiple genres per show, separate into individual rows
    df["genres"] = df["genres"].str.split(", ")

    # Each genre in its own row
    df = df.explode("genres")

    # Remove invalid rows that have 0 or 1 episodes
    df = df[df["number_of_episodes"] > 100]

    # Group and count by genre
    grouped = df.groupby("genres").size().reset_index(name="Total Shows")

    # Sort descending and keep only the first 10
    grouped = grouped.sort_values(by="Total Shows", ascending=False).head(10)

    # Add a title
    print("\nGenres with the most long-running shows\n")

    # Display results
    print(grouped.to_string(index=False))


    # Style graph visualization

    # Set a figure size
    plt.figure(figsize=(10, 6))

    # Unique color list for each genre using the color picker
    colors = [
        "#0077B6", "#B4D873", "#E7EF1B", "#48CAE4", "#ADE8F4",
        "#F4A300", "#E63946", "#9C27B0", "#00B050", "#6A994E"
    ]

    # Create each horizontal bar individual bar to use a bar chart horizontally
    bars = plt.barh(grouped["genres"], grouped["Total Shows"], color=colors)

    # Adjust the x-axis label
    plt.xlabel("Total Shows", fontsize=14, fontweight="bold")

    # Adjust the y-axis label
    plt.ylabel("Genres", fontsize=14, fontweight="bold")

    # Adjust a title for the bar chart (spaces are left on purpose to align the title with the graph correctly)
    plt.title("                     Top 10 Genres with the Most Long-Running TV Shows (over 100 episodes)",
              fontsize=15, fontweight="bold", color="#004D7A")

    # Add a legend
    plt.legend(bars, grouped["genres"], title = "Genres", loc = "center left", bbox_to_anchor=(1.07, 0.5))

    # Due to a legend being applied, remove the ticks on the x-axis to avoid conflict when visualizing the graph
    plt.yticks([])

    # Allows the axis labels to be displayed correctly
    plt.tight_layout()

    # Display the graph
    plt.show()


# Fifth Query: Which decades have produced the most TV shows?

def shows_per_decade():

    # Load filtered dataset
    df = filtered_data()

    # Keep relevant columns
    df = df[["Year", "name"]]

    # Create a new column for the decade by dividing each year by 10, discarding the decimals and multiplying by 10
    # to obtain the number rounded to the decade
    df["Decade"] = (df["Year"] // 10) * 10

    # Group by decade and count total shows
    grouped = df.groupby("Decade").size().reset_index(name="Total TV Shows")

    # Sort by descending order and show only the first 5
    grouped = grouped.sort_values(by="Total TV Shows", ascending=False).head(5)

    # Add a title
    print("\nTop 5 Decades with the Most TV Show Releases\n")

    # Print results
    print(grouped.to_string(index=False))


    # Style graph visualization

    # Set a figure size for the graph
    plt.figure(figsize=(10, 6))

    # Unique color list for each genre using the color picker
    colors = [
        "#0077B6", "#B4D873", "#E7EF1B", "#48CAE4", "#ADE8F4",
    ]

    # Create vertical bars individually with labels to use a bar plot
    bars = plt.bar(grouped["Decade"].astype(str) + "s", grouped["Total TV Shows"], color=colors)

    # Add a title
    plt.title("Top 5 Decades with the Most TV Show Releases",
              fontsize=18, fontweight="bold", color="#004D7A")

    # Adjust the x-axis label
    plt.xlabel("Decades", fontsize=14, fontweight="bold")

    # Adjust the y-axis label
    plt.ylabel("Total TV Shows", fontsize=14, fontweight="bold")

    # Add a legend for the graph
    plt.legend(bars, grouped["Decade"].astype(str)+ "s", title="Decades", loc = "center left",
               bbox_to_anchor=(1.07, 0.5), fontsize = 14, title_fontsize=18)

    # Due to a legend being applied, remove the ticks on the x-axis to avoid conflict when visualizing the graph
    plt.xticks([])

    # Adjust the graph to avoid cuts
    plt.tight_layout()

    # Display graph
    plt.show()

# Filter warning message
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

#Run all graphs
def guillermo_graph():
    tv_shows_per_year()
    language_percentage()
    avg_rating_by_genre()
    genres_with_long_shows()
    shows_per_decade()


