import datetime
import pandas as pd
from util import make_snake_case, extract_character_before_delimeter, get_episode_code, process_dim_fields, process_fact_fields, export_df_to_csv



# Part 1: Extract data from Wikipedia
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_Glee_episodes')
seasons = data[0]
episodes = pd.DataFrame()
for season in range(1, 6+1):
    df = data[season]
    df['season'] = season
    episodes = pd.concat([episodes, df])



# Part 2: Transform seasons ====================================================
# Flatten multi-row column names
seasons.columns = [column[1] for column in seasons.columns]

# Make columns snake case
seasons.columns = map(make_snake_case, seasons.columns)

# Drop Episodes.1
seasons = seasons.drop(['episodes.1'], axis=1)

# Extract number for [ in rank
seasons['rank'] = seasons['rank'].apply(lambda x: extract_character_before_delimeter(x, '['))

# Convert First aired and last_aired into datetime
seasons['first_aired'] = pd.to_datetime(seasons['first_aired'])
seasons['last_aired'] = pd.to_datetime(seasons['last_aired'])

# Convert rank into integer
seasons['rank'] = seasons['rank'].astype('int64')



# Part 3: Transform episodes ===================================================
# Make columns into snake case
episodes.columns = map(make_snake_case, episodes.columns)

# Remove the first and last characters in Title
episodes['title'] = episodes['title'].apply(lambda x: x[1:-1])

# Replace value
episodes['written_by'] = episodes['written_by'].replace(
    {"Story by : Ryan Murphy & Tim WollastonTeleplay by : Ryan Murphy": "Ryan Murphy & Tim Wollaston"}
)

# Remove [nb] in original_air_date; Convert to datetime
episodes['original_air_date'] = episodes['original_air_date'].str.replace(r'\[.*\]', '')
episodes['original_air_date'] = pd.to_datetime(episodes['original_air_date'])

# Remove [] in US viewers
episodes['us_viewers(millions)'] = episodes['us_viewers(millions)'].apply(lambda x: extract_character_before_delimeter(x, '['))

# Add episode_code
episodes['episode_code'] = episodes[['season', 'no._inseason']].apply(lambda x: get_episode_code(*x), axis=1)

# Add primary key
episodes['episode_id'] = range(1, len(episodes)+1)

# Keep only necessary columns
episodes = episodes[[
    'episode_id', 'no.overall', 'episode_code', 'season', 'no._inseason', 'title', 
    'directed_by', 'written_by', 'original_air_date', 'us_viewers(millions)'
]]

# Rename columns
episodes = episodes.rename(
    columns={
        'no.overall': 'overall', 
        'no._inseason': 'episode', 
        'title': 'episode_title', 
        'us_viewers(millions)': 'viewer_count'
    }
)

# Change data types
episodes['viewer_count'] = episodes['viewer_count'].astype('float64')



# # Part 4: Transform directors ==================================================
directors = process_dim_fields(
    df=episodes[['directed_by']],
    primary_key='director_id',
    col_to_rename={'directed_by': 'director_name'},
    col_order=['director_id', 'director_name']
)



# # Part 5: Transform episode writers
episode_writers = process_fact_fields(
    df=episodes[['written_by']],
    primary_key='episode_writer_id',
    col_to_rename={'written_by': 'writers'},
    split_col_name='writer_name',
    col_to_split='writers',
    delimeter=' & '
)



# Part 6: Writers
writers = process_dim_fields(
    df=episode_writers[['writer_name']],
    primary_key='writer_id',
    col_order=['writer_id', 'writer_name']
)



# Part 7: Create foreign keys ==================================================
# Merge dataframes
episodes = pd.merge(episodes, directors, left_on='directed_by', right_on='director_name')
episodes = pd.merge(episodes, episode_writers, left_on='written_by', right_on='writers')
episodes = episodes.drop_duplicates(subset=['episode_id']).reset_index(drop=True)
episode_writers = pd.merge(episode_writers, writers, on='writer_name')

# Keep only required columns
episodes = episodes[[
    'episode_id', 'overall', 'episode_code', 'season', 'episode',
    'episode_title', 'director_id', 'episode_writer_id', 
    'original_air_date', 'viewer_count'
]]
episode_writers = episode_writers[['episode_writer_id', 'writer_id']]



# Part 8: Export data as CSV
# export_df_to_csv(episodes, 'dim_episodes')
# export_df_to_csv(directors, 'dim_directors')
# export_df_to_csv(episode_writers, 'fact_episode_writer')
# export_df_to_csv(writers, 'dim_writers')
