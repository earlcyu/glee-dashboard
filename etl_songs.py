import numpy as np
import pandas as pd 
from util import make_snake_case, extract_character_before_delimeter, get_episode_code, process_dim_fields, process_fact_fields, export_df_to_csv



# Part 1: Extract data from Wikipedia ==========================================
# Create a list of links (one for each season of Glee)
links = [f'https://en.wikipedia.org/wiki/List_of_songs_in_Glee_(season_{link})' for link in range(1, 6+1)]

# Extract data from each link and store as a dataframe
songs = pd.DataFrame()
for index, link in enumerate(links):
    df = pd.read_html(link)[0]
    df['season'] = index + 1
    songs = pd.concat([songs, df])



# Part 2: Trasnform data =======================================================
# Make column names into snake case
songs.columns = map(make_snake_case, songs.columns)

# Clean album column
songs['album'] = songs['album'].fillna(songs['album[nb_1]']).fillna('N/A')
songs['album'] = songs['album'].replace(
    {
        '—': 'N/A', 
        'TBA': 'N/A',
        "The Untitled Rachel Berry Project''": "The Untitled Rachel Berry Project",
        "The Complete Season Four[5]": "The Complete Season Four",
    }
)

# Clean performed_by column
songs['performed_by'] = songs['performed_by'].replace(
    to_replace={
        ' and': ',',
        ' with': ',',
        ';': ', ',
        ',and': ', ',
        ',J': ', J',
        '  ': ' ',
        'Brody  Weston': 'Brody Weston',
        ',,': ',',
        'Changand': 'Chang, ',
        ':': ',',
        '(instrumental version only)': '',
        'Brittany Pierce': 'Brittany S. Pierce',
        ' as Rachel Berry': '',
        'Unique Adams': 'Unique "Wade" Adams',
        'the': 'The'
    },
    regex=True
)

# Remove the first and last quotation marks from the title column
songs['title'] = songs['title'].str[1:-1]

# Extract episode number
songs['episode'] = songs['episode'].apply(lambda x: extract_character_before_delimeter(x, '.'))

# Replace Yes/No with True/False in the Single column
songs['single'] = songs['single'].replace({'Yes': True, 'No': False})

# Add a primary key column
songs['song_id'] = range(1, len(songs)+1)

# Get the episode_code by combining Season and episode
songs['episode_code'] = songs[['season', 'episode']].apply(lambda x: get_episode_code(*x), axis=1)

# Remove Season, episode, Album
songs = songs.drop(['ref.', 'season', 'episode'], axis=1)

# Rename columns
songs = songs.rename(columns={'title': 'song_title', 'single': 'is_single'})



# Part 3: Covers ===============================================================
# Drop duplicates; Add a primary key column; Rename; Re-order
covers = process_dim_fields(
    df=songs[['version_covered']], 
    primary_key='cover_id', 
    col_to_rename={'version_covered': 'cover_name'},
    col_order=['cover_id', 'cover_name']
)



# Part 4: Albums ===============================================================
# Drop duplicates; Add a primary key column; Rename; Re-order
albums = process_dim_fields(
    df=songs[['album']],
    primary_key='album_id',
    col_to_rename={'album': 'album_name'},
    col_order=['album_id', 'album_name']
)



# # Part 5: Song Performers=======================================================
song_performers = process_fact_fields(
    df=songs[['performed_by']],
    primary_key='song_performer_id',
    col_to_rename={'performed_by': 'performers'},
    split_col_name='performer_name',
    col_to_split='performers',
    delimeter=', '
)



# # Part 6: Performers ===========================================================
# Drop duplicates; Add a primary key column
performers = process_dim_fields(
    df=song_performers[['performer_name']], 
    primary_key='performer_id',
    col_order=['performer_id', 'performer_name']
)



# Part 7: Create foreign keys ==================================================
# Merge dataframes
songs = pd.merge(songs, covers, left_on='version_covered', right_on='cover_name')
songs = pd.merge(songs, albums, left_on='album', right_on='album_name')
songs = pd.merge(songs, song_performers, left_on='performed_by', right_on='performers')
songs = songs.drop_duplicates(subset=['song_id']).reset_index(drop=True)
song_performers = pd.merge(song_performers, performers, on='performer_name')

# Keep only required columns
songs = songs[[
    'song_id', 'episode_code', 'song_title', 'cover_id', 
    'song_performer_id', 'album_id'
]]
song_performers = song_performers[[
    'song_performer_id', 'performer_id'
]]



# Part 8: Export data as CSV ===================================================
# export_df_to_csv(songs, 'dim_songs')
# export_df_to_csv(covers, 'dim_covers')
# export_df_to_csv(albums, 'dim_albums')
# export_df_to_csv(song_performers, 'fact_song_performers')
# export_df_to_csv(performers, 'dim_performers')
