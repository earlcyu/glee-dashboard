import pandas as pd 



songs_df = pd.DataFrame()

for season in range(1,6+1):
    url = f'https://en.wikipedia.org/wiki/List_of_songs_in_Glee_(season_{season})'
    # Extract the first table in the web page 
    df = pd.read_html(url)[0] 
    # Add a new column in indicate the season 
    df['season'] = season 
    # Concatenate the dataframe to the main songs dataframe 
    songs_df = pd.concat([songs_df, df], ignore_index=True) 

# songs_df.to_csv('data/raw_songs.csv', index=False)
