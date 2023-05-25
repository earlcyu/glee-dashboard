import numpy as np
import pandas as pd 
from util import extract_character_before_delimeter, get_episode_code, process_dim_fields, process_fact_fields, export_df_to_csv



# Part 1: Extract data from Wikipedia ==========================================
# Create a list of links (one for each season of Glee)
links = [f'https://en.wikipedia.org/wiki/List_of_songs_in_Glee_(season_{link})' for link in range(1, 6+1)]

# Extract data from each link and store as a dataframe
songs = pd.DataFrame()
for index, link in enumerate(links):
    df = pd.read_html(link)[0]
    df['Season'] = index + 1
    songs = pd.concat([songs, df])



# Part 2: Trasnform data =======================================================
# Clean Album column
songs['Album'] = songs['Album'].fillna(songs['Album[nb 1]']).fillna('N/A')
songs['Album'] = songs['Album'].replace(
    {
        '—': 'N/A', 
        'TBA': 'N/A',
        "The Untitled Rachel Berry Project''": "The Untitled Rachel Berry Project",
        "The Complete Season Four[5]": "The Complete Season Four",
    }
)

# Clean Performed by column
songs['Performed by'] = songs['Performed by'].replace(
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

# Remove the first and last quotation marks from the Title column
songs['Title'] = songs['Title'].apply(lambda x: x[1:-1])

# Extract episode number
songs['Episode'] = songs['Episode'].apply(lambda x: extract_character_before_delimeter(x, '.'))

# Replace Yes/No with True/False in the Single column
songs['Single'] = songs['Single'].replace({'Yes': True, 'No': False})

# Add a primary key column
songs['Song ID'] = range(1, len(songs)+1)

# Get the Episode Code by combining Season and Episode
songs['Episode Code'] = songs[['Season', 'Episode']].apply(lambda x: get_episode_code(*x), axis=1)

# Remove Season, Episode, Album
songs = songs.drop(['Ref.', 'Season', 'Episode'], axis=1)

# Rename columns
songs = songs.rename(columns={'Title': 'Song Title', 'Single': 'Is Single'})



# Part 3: Covers ===============================================================
covers = songs[['Version covered']]

# Drop duplicates; Add a primary key column
covers = process_dim_fields(covers, 'Cover ID')

# Rename column
covers = covers.rename(columns={'Version covered': 'Version Covered Name'})

# Re-order columns
covers = covers[['Cover ID', 'Version Covered Name']]



# Part 4: Albums ===============================================================
albums = songs[['Album']]

# Drop duplicates; Add a primary key column
albums = process_dim_fields(albums, 'Album ID')

# Rename column
albums = albums.rename(columns={'Album': 'Album Name'})

# Re-order columns
albums = albums[['Album ID', 'Album Name']]



# Part 5: Song Performers=======================================================
song_performers = process_fact_fields(
    df=songs[['Performed by']],
    primary_key='Song Performer ID',
    split_col_name='Performer Name',
    col_to_split='Performed By',
    delimeter=', '
)

# Re-order columns
song_performers = song_performers[['Song Performer ID', 'Performed By']]



# Part 6: Performers ===========================================================
performers = song_performers

# Drop duplicates; Add a primary key column
performers = process_dim_fields(performers[['Performer Name']], 'Performer ID')

# Re-order columns
performers = performers[['Performer ID', 'Performer Name']]



# Part 7: Create foreign keys ==================================================
# Merge dataframes
songs = pd.merge(songs, covers, left_on='Version covered', right_on='Version Covered Name')
songs = pd.merge(songs, albums, left_on='Album', right_on='Album Name')
songs = pd.merge(songs, song_performers, left_on='Performed by', right_on='Performed By')
songs = songs.drop_duplicates(subset=['Song ID']).reset_index(drop=True)
song_performers = pd.merge(song_performers, performers, on='Performer Name')

# Keep only required columns
songs = songs[[
    'Song ID', 'Episode Code', 'Song Title', 'Cover ID', 'Song Performer ID', 
    'Is Single', 'Album ID'
]]
song_performers = song_performers[['Song Performer ID', 'Performer ID']]



# Part 8: Export data as CSV ===================================================
# export_df_to_csv(songs, 'dim_songs')
# export_df_to_csv(covers, 'dim_covers')
# export_df_to_csv(albums, 'dim_albums')
# export_df_to_csv(song_performers, 'fact_song_performers')
# export_df_to_csv(performers, 'dim_performers')
