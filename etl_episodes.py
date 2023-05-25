import datetime
import pandas as pd
from util import remove_first_and_last_characters, extract_character_before_delimeter, get_episode_code, process_dim_fields, process_fact_fields



# Part 1: Extract data from Wikipedia
data = pd.read_html('https://en.wikipedia.org/wiki/List_of_Glee_episodes')
seasons = data[0]
episodes = pd.DataFrame()
for season in range(1, 6+1):
    df = data[season]
    df['Season'] = season
    episodes = pd.concat([episodes, df])



# Part 2: Transform seasons ====================================================
# Flatten multi-row column names
seasons.columns = [column[1] for column in seasons.columns]

# Drop Episodes.1
seasons = seasons.drop(['Episodes.1'], axis=1)

# Extract number for [ in Rank
seasons['Rank'] = seasons['Rank'].apply(lambda x: extract_character_before_delimeter(x, '['))

# Convert First aired and Last aired into datetime
seasons['First aired'] = pd.to_datetime(seasons['First aired'])
seasons['Last aired'] = pd.to_datetime(seasons['Last aired'])

# Convert Rank into integer
seasons['Rank'] = seasons['Rank'].astype('int64')



# Part 3: Transform episodes ===================================================
# Remove the first and last characters in Title
episodes['Title'] = episodes['Title'].apply(lambda x: x[1:-1])

# Replace value
episodes['Written by'] = episodes['Written by'].replace(
    {"Story by : Ryan Murphy & Tim WollastonTeleplay by : Ryan Murphy": "Ryan Murphy & Tim Wollaston"}
)

# Remove [nb] in Original air date; Convert to datetime
episodes['Original air date'] = episodes['Original air date'].str.replace(r'\[.*\]', '')
episodes['Original air date'] = pd.to_datetime(episodes['Original air date'])

# Remove [] in US viewers
episodes['US viewers(millions)'] = episodes['US viewers(millions)'].apply(lambda x: extract_character_before_delimeter(x, '['))

# Add Episode Code
episodes['Episode Code'] = episodes[['Season', 'No. inseason']].apply(lambda x: get_episode_code(*x), axis=1)

# Add primary key
episodes['Episode ID'] = range(1, len(episodes)+1)

# Keep only necessary columns
episodes = episodes[[
    'Episode ID', 'No.overall', 'Episode Code', 'Season', 'No. inseason', 'Title', 
    'Directed by', 'Written by', 'Original air date', 'US viewers(millions)'
]]

# Rename columns
episodes = episodes.rename(
    columns={
        'No.overall': 'Overall', 
        'No. inseason': 'Episode', 
        'Title': 'Episode Title', 
        'US viewers(millions)': 'US Viewer Count (in millions)'
    }
)

# Change data types
episodes['US Viewer Count (in millions)'] = episodes['US Viewer Count (in millions)'].astype('float64')



# Part 4: Transform directors ==================================================
directors = episodes[['Directed by']]

# Drop duplicates; Add primary key column
directors = process_dim_fields(directors, 'Director ID')

# Rename column
directors = directors.rename(columns={'Directed by': 'Director Name'})

# Re-order columns
directors = directors[['Director ID', 'Director Name']]



# Part 5: Transform episode writers
episode_writers = process_fact_fields(
    df=episodes[['Written by']],
    primary_key='Episode Writer ID',
    split_col_name='Writer Name',
    col_to_split='Written By',
    delimeter=' & '
)



# Part 6: Writers
writers = process_dim_fields(episode_writers[['Writer Name']], 'Writer ID')

writers = writers[['Writer ID', 'Writer Name']]

print(writers)
