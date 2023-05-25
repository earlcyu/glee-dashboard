import numpy as np
import pandas as pd

def remove_first_and_last_characters(string):
    return string[1:-1]

def extract_character_before_delimeter(string, delimeter):
    position = string.find(delimeter)
    return string[:position]
    
def get_episode_code(season, episode):
    if len(str(episode)) == 1:
        return f'S0{str(season)}E0{episode}'
    else:
        return f'S0{str(season)}E{episode}'

def process_dim_fields(df: pd.DataFrame, field):
    df = df.drop_duplicates().reset_index(drop=True)
    df[field] =  range(1, len(df)+1)
    return df

def process_fact_fields(df: pd.DataFrame, primary_key, split_col_name, col_to_split, delimeter):
    df[primary_key] = range(1, len(df)+1)
    df.columns = df.columns.str.title()
    df[split_col_name] = df[col_to_split].str.split(delimeter)
    df = df.explode(split_col_name)
    df[split_col_name] = df[split_col_name].str.strip()
    return df


def export_df_to_csv(df, filename, directory='data'):
    df.to_csv(f'{directory}/{filename}.csv', index=False)