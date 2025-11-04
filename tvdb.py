import mariadb
import pandas as pd
import matplotlib.pyplot as plt

DB_CONFIG = {
    'host': 'localhost',
    'user': 'coen2220',
    'password': 'coen2220',
    'database': 'group01',
    'port': 3306,
}

#coonnects to MariaDB, reads the columns we only assigned, cleans data and removes dupes of the shows, returns clean pandas Dataframe
def load_clean_df():
    
    cols = [
        "id","name","original_language","first_air_date",
        "vote_average","vote_count","number_of_seasons","number_of_episodes","genres"
    ]
    conn = None
    #opens MariaDB conection and reads the table into panas
    try:
        conn = mariadb.connect(**DB_CONFIG)
        df = pd.read_sql(f"SELECT {', '.join(cols)} FROM `tvshows`", conn)
    finally:
        if conn:
            conn.close()
    
    #detects duplicates
    df["norm_name"] = (df["name"]
                       .fillna("")
                       .str.strip()
                       .str.lower())

    #drops rows where the date is missing
    df = df[ df["first_air_date"].notna() ]
    df = df[df["first_air_date"].astype(str).ne("0000-00-00")]
    
    #converts to real datetime
    df["first_air_date"] = pd.to_datetime(df["first_air_date"], errors="coerce")
    df = df.dropna(subset=["first_air_date"])

    #converts to rating columns to numeric so we can do math
    df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
    df["vote_count"]   = pd.to_numeric(df["vote_count"],   errors="coerce").fillna(0).astype(int)
    #seasons to int
    df["number_of_seasons"]  = pd.to_numeric(df["number_of_seasons"], errors="coerce").fillna(0).astype(int)
    #episodes to int
    df["number_of_episodes"] = pd.to_numeric(df["number_of_episodes"], errors="coerce").fillna(0).astype(int)

    
    #removes the duplicate shows
    #sorts the row with the biggest vote stays first
    df = (df.sort_values("vote_count", ascending=False)         
            .drop_duplicates(subset=["norm_name","first_air_date","original_language"], keep="first")
            .reset_index(drop=True))

    return df

#loads clean data
df_clean = load_clean_df()
print(f" Clean rows: {len(df_clean):,}")


#languages we use (top10)
LANGS = ['en','es','zh','hi','ar','fr','pt','ru','ja','de']
LANG_NAMES = {'en':'English','es':'Spanish','zh':'Chinese','hi':'Hindi','ar':'Arabic',
              'fr':'French','pt':'Portuguese','ru':'Russian','ja':'Japanese','de':'German'}

#1)What is the average TV show rating by the original language?
q1 = (df_clean[df_clean["original_language"].isin(LANGS)]
        .dropna(subset=["vote_average"])
        .groupby("original_language")
        .agg(avg_rating=("vote_average","mean"),
             shows_in_lang=("id","count"))
        .reset_index())


q1 = (q1.set_index("original_language")
         .reindex(LANGS)               
         .dropna(how="any")            
         .reset_index())
q1["Language"] = q1["original_language"].map(LANG_NAMES).fillna(q1["original_language"])

import matplotlib.ticker as mticker
plt.figure(figsize=(12,6))
plt.bar(q1["Language"], q1["avg_rating"], label="Average rating")
plt.title("Average TV Show Rating by Major Languages")
plt.xlabel("Language"); plt.ylabel("Average Rating"); plt.ylim(0,10)
plt.xticks(rotation=20, ha="right")

#labels each bar with number of shows
for i,(r,n) in enumerate(zip(q1["avg_rating"], q1["shows_in_lang"])):
    plt.text(i, r+0.08, f"{int(n):,}", ha="center", va="bottom", fontsize=9)
plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=False))
plt.legend(loc="best")
plt.tight_layout(); plt.show()


#2)Which genres have the most tv shows?
q2 = (df_clean.dropna(subset=["genres"]) #keeps rows with genres only
        .assign(genres=df_clean["genres"].str.split(",")) #makes one row per genre     
        .explode("genres") #reomves extra space in genre names                                      
        .assign(genres=lambda d: d["genres"].str.strip()) #count shows per genre      
        .groupby("genres").size().reset_index(name="total_shows") #sorts from biggest to smallest genre
        .sort_values("total_shows", ascending=False) #takes only the top10 genres
        .head(10))

plt.figure(figsize=(12,6))
plt.bar(q2["genres"], q2["total_shows"], label="Total Shows by Genre")
plt.title("Top 10 TV Show Genres")
plt.xlabel("Genre"); plt.ylabel("Number of TV Shows")
plt.xticks(rotation=30, ha="right")

#puts exact count on top of each bar
for i, v in enumerate(q2["total_shows"]):
    plt.text(i, v + max(q2["total_shows"])*0.01, f"{int(v):,}", ha="center", va="bottom", fontsize=9)
plt.legend(loc="best")
plt.tight_layout(); plt.show()



#3)Which are the 10 highest-rated TV shows
q3 = (df_clean.dropna(subset=["vote_average"])
        .query("vote_count >= 100")
        .sort_values(["vote_average","vote_count"], ascending=[False, False])
        .loc[:, ["name","vote_average","vote_count","original_language"]]
        .head(10))

#I used vote_count as the size so bigger shows take more of the pie space
sizes  = q3["vote_count"].clip(lower=1) 
labels = q3["name"]

plt.figure(figsize=(10,8))
plt.pie(sizes, labels=None, autopct="%1.0f%%", startangle=140, textprops={'fontsize': 15})
plt.title("Top 10 Highest-Rated Shows Share of Vote Count")

#shows the show names on the side
plt.legend(labels, title="TV Shows", loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10, title_fontsize=11)
plt.tight_layout(); plt.show()


#7)Is there a correlation between the number of seasons and total number of episodes?
q7 = df_clean.query("number_of_seasons > 0 and number_of_episodes > 0")

#groups the shows into buckets like 1-2 seasons or more
bins   = [1, 3, 6, 11, 21, 10_000]
labels = ["1–2", "3–5", "6–10", "11–20", "21+"]

q7_bins = pd.cut(
    df_clean["number_of_seasons"].clip(lower=0),
    bins=bins, labels=labels, right=False
)
counts = q7_bins.value_counts().reindex(labels).fillna(0)

plt.figure(figsize=(9,8))
plt.pie(counts, labels=None, autopct="%1.1f%%", startangle=140, textprops={'fontsize': 15})
plt.title("Distribution of TV Shows by Season Count")
plt.legend(labels, title="Seasons", loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10, title_fontsize=11)
plt.tight_layout(); plt.show()

#prints the numerical correlation
print("Pearson corr:\n", q7[["number_of_seasons","number_of_episodes"]].corr())


#8)Which are the TV shows with the largest number of seasons?
q8 = (df_clean.sort_values(["number_of_seasons","number_of_episodes"], ascending=False)
        .loc[:, ["name","number_of_seasons","number_of_episodes","original_language"]]
        .head(10))

sizes  = q8["number_of_seasons"].clip(lower=1)  #each pie slice = number of seasons 
labels = q8["name"] #names for the legend

plt.figure(figsize=(10,8))
plt.pie(sizes, labels=None, autopct="%1.1f%%", startangle=140, textprops={'fontsize': 15})
plt.title("Top 10 TV Shows by Seasons")
plt.legend(labels, title="TV Shows", loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10, title_fontsize=11)
plt.tight_layout(); plt.show()

