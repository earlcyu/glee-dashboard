import math 
import pandas as pd 
from util import convert_to_snake_case, get_album



songs_df = pd.read_csv('data/raw_songs.csv')

# Make column names into snake case
songs_df.columns = list(map(convert_to_snake_case, songs_df.columns))

# Drop `ref`
songs_df.drop(columns=['ref.'], axis=1, inplace=True) 

# Remote quotation makrs in `title`
songs_df['title'] = songs_df['title'].str.replace('"', '')

# Extract episode number from `episode`
songs_df['episode'] = songs_df['episode'].apply(lambda x: x[:x.find('.')])

# Handle null values in `album`
songs_df['album'] = songs_df[['album[nb_1]', 'album']].apply(
    lambda x: get_album(*x), axis=1
)
songs_df.drop(columns=['album[nb_1]'], inplace=True) 

# Replace some values in `album`
album_replacements = {
    '—': math.nan,
    "Movin' Out": 'Movin Out',
    'The Complete Season Four[5]': 'The Complete Season Four', 
    "The Untitled Rachel Berry Project''": 'The Untitled Rachel Berry Project' 
}
songs_df['album'].replace(album_replacements, inplace=True) 
songs_df['album'].replace('\xa0', ' ', inplace=True, regex=True)

# Add a primary key column
songs_df['song_id'] = list(range(1, songs_df.shape[0]+1))

# Replace some values in `performed by`
performed_by_replacements = {
    ' and': ',',
    ' with': ',',
    ':': ',',
    ',and': ', ',
    ',J': ', J',
    '  ': ' ',
    'Brody  Weston': 'Brody Weston',
    ',,': ',',
    'Changand': 'Chang, ',
    '(instrumental version only)': ''
}

songs_df['performed_by'].replace(performed_by_replacements, inplace=True)

# Load transformed data 
# songs_df.to_csv('data/transformed_songs.csv', index=False, sep='|')
