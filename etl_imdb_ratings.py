import pandas as pd 
from util import get_episode_code 



# Load the raw TSV file containing all episodes 
episodes_df = pd.read_csv('data/src/imdb_episodes.tsv', sep='\t')
# Filter `episodes_df` to only include episodes from Glee 
# I had to load the `akas` TSV file ad-hoc to determine Glee's parentTconst 
glee_episodes_df = episodes_df[episodes_df['parentTconst'] == 'tt1327801']
# Load the raw TSV file containing the ratings for all episodes of all TV shows
ratings_df = pd.read_csv('data/src/imdb_ratings.tsv', sep='\t')
# Perform an inner join to get only Glee's ratings
glee_ratings_df = pd.merge(
    glee_episodes_df, 
    ratings_df, 
    how='inner', 
    left_on='tconst',
    right_on='tconst'
)
# Apply a function to get the episode code, which will be used as a join key 
# for dim_episodes.csv 
glee_ratings_df['episode_code'] = glee_ratings_df[['seasonNumber', 'episodeNumber']].apply(lambda x: get_episode_code(*x), axis=1)
# Export the file 
glee_ratings_df.to_csv('data/transformed/fact_episode_ratings.csv', index=False)
