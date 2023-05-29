import numpy as np
import pandas as pd

def make_snake_case(string):
    return string.lower().replace(' ', '_')

def extract_character_before_delimeter(string, delimeter):
    position = string.find(delimeter)
    return string[:position]
    
def get_episode_code(season, episode):
    if len(str(episode)) == 1:
        return f'S0{str(season)}E0{episode}'
    else:
        return f'S0{str(season)}E{episode}'

def process_dim_fields(df: pd.DataFrame, primary_key, col_to_rename=None, col_order=None):
    # Drop duplicates; Reset index
    df = df.drop_duplicates(ignore_index=True)
    # Add a primary key
    df[primary_key] =  range(1, len(df)+1)
    # Rename columns
    if col_to_rename:
        df = df.rename(columns=col_to_rename)
    # Re-order columns
    df = df[col_order]
    return df

def process_fact_fields(df: pd.DataFrame, primary_key, split_col_name, col_to_split, delimeter, col_to_rename=None, col_order=None):
    # Drop duplicates; Reset index
    df = df.drop_duplicates(ignore_index=True)
    # Add a primary key    
    df[primary_key] = range(1, len(df)+1)
    # Rename columns
    if col_to_rename:
        df = df.rename(columns=col_to_rename)
    # Split column
    df[split_col_name] = df[col_to_split].str.split(delimeter)
    # Explode column
    df = df.explode(split_col_name)
    df[split_col_name] = df[split_col_name].str.strip()
    # Re-order columns
    if col_order:
        df = df[col_order]
    return df


def export_df_to_csv(df, filename, directory='data'):
    df.to_csv(f'{directory}/{filename}.csv', index=False)
