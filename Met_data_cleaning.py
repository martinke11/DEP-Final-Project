#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pycountry
import os
os.chdir('/Users/mitalidighe/Desktop/UChicago Quarter 1/DEP/Final project/MoMA/Final Presentation')

df = pd.read_csv('MetObjects.csv')

# deleted 'Constinuent ID' because it wasnt unique and created a unique key using a function

columns_to_drop = ['Constituent ID', 'Object Number', 'Gallery Number', 'Portfolio', 'Artist Prefix', 'Artist Display Bio',
                   'Artist Suffix', 'Artist Alpha Sort', 'Artist ULAN URL', 'Artist Wikidata URL', 'Object Date',
                   'Classification', 'Rights and Reproduction', 'Link Resource', 'Object Wikidata URL',
                   'Metadata Date', 'Repository', 'Tags', 'Tags AAT URL', 'Tags Wikidata URL']

df.drop(columns=columns_to_drop, inplace=True)

# Dropping rows with no Title, and other redundant column values
def drop_missing_values(df):
    """
    Remove rows with missing values in specific columns of the DataFrame.

    Args:
    df (pandas.DataFrame): The DataFrame from which rows with missing values will be removed.

    Returns:
    pandas.DataFrame: The DataFrame after removing rows with missing values in specified columns.
    """
    columns_to_check = ['Title', 'AccessionYear', 'Object Name', 'Medium', 'Credit Line', 'Dimensions']
    for column in columns_to_check:
        df.dropna(subset=[column], inplace=True)
    
    return df


df = drop_missing_values(df)

df.isna().sum()

string_columns = [
    "Culture", "Period", "Dynasty", "Reign", 
    "Artist Role", "Artist Display Name", "City", "State", 
    "County", "Country", "Region", "Subregion", 
    "Locale", "Locus", "Excavation", "River"
]

columns_to_convert = ['Is Highlight', 'Is Timeline Work', 'Is Public Domain']

def process_dataframe(df, string_columns, columns_to_convert):
    """
    Process the DataFrame by changing data types, renaming columns, handling missing values, and cleaning string columns.

    Args:
    df (pandas.DataFrame): The DataFrame to be processed.
    string_columns (list of str): List of string columns to clean.
    columns_to_convert (list of str): List of boolean columns to convert to 0/1.

    Returns:
    pandas.DataFrame: The processed DataFrame.
    """
    # Change datatype to year
    df['AccessionYear'] = pd.to_datetime(df['AccessionYear'], errors='coerce').dt.year
    df['AccessionYear'] = df['AccessionYear'].fillna(0).astype(int)

    #Change data types
    df['Artist Begin Date'] = pd.to_datetime(df['Artist Begin Date'], errors='coerce').dt.year
    df['Artist End Date'] = pd.to_datetime(df['Artist End Date'], errors='coerce').dt.year
    
    df['Artist Begin Date'] = df['Artist Begin Date'].fillna(0).astype(int)
    df['Artist End Date'] = df['Artist End Date'].fillna(0).astype(int)
    
    ## Assumed that the Nationality data is filled according to country naming conventions
    df['Artist Nationality'] = df['Artist Nationality'].str.split('|').str[0].str.strip()
    df['Artist Nationality'] = df['Artist Nationality'].str.capitalize()

    # Artist gender - is female flag
    df.rename(columns={'Artist Gender': 'Is Female'}, inplace=True)
    df['Is Female'] = df['Is Female'].apply(lambda x: 0 if pd.isnull(x) else 1)

    # Artist Role cleaning
    df['Artist Role'] = df['Artist Role'].str.split('|').str[0]
    
    # Geography cleaning
    df['geography_type'] = df['geography_type'].str.split('|').str[0]
    df['geography_type'].fillna('Unknown', inplace=True)

    # Converting boolean columns to 0/1
    for col in columns_to_convert:
        df[col] = df[col].apply(lambda x: 0 if x == False else 1)
    
    # Cleaning string columns
    for col in string_columns:
        df[col] = df[col].str.strip()
        df[col] = df[col].replace('', 'Unknown')
        df[col] = df[col].replace('nan', 'Unknown')
        df[col] = df[col].fillna('Unknown')

    return df


df = process_dataframe(df, string_columns, columns_to_convert)


#Clean countries columns
countries = [country.name for country in pycountry.countries]

def find_country(row):
    if isinstance(row, str):  # Check if the value is a string
        for country in countries:
            if country in row:
                return country
    return 'Unknown'  # Return 'NA' for NaN or non-string values


df['Artist Nationality'] = df['Artist Nationality'].apply(find_country)   

def find_country(row):
    for country in countries:
        if country in row:
            return country
    return 'Unknown'


df['Country'] = df['Country'].apply(find_country)


def clean_dataframe(df):
    """
    Cleans the DataFrame by checking string columns for non-ASCII or numeric values, normalizing text data to lowercase, and removing duplicate rows.

    Args:
    df (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
    pandas.DataFrame: The cleaned DataFrame.
    int: The number of rows removed as duplicates.
    """
    # Checking all the string columns for absurd values
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna('Unknown')  # Replace NaN with 'Unknown'
        df[col] = df[col].str.strip()        # Strip white spaces
        df[col] = df[col].apply(lambda x: 'Unknown' if not x.isascii() or x.isnumeric() else x)
    
    # Normalizing Text Data
    string_columns = df.select_dtypes(include='object').columns
    df[string_columns] = df[string_columns].apply(lambda x: x.str.lower())

    return df


df = clean_dataframe(df)


def format_column_names(df):
    """
    Formats the column names of a DataFrame to snake_case, removes spaces, and renames specific columns.

    Args:
    df (pandas.DataFrame): The DataFrame whose column names are to be formatted.

    Returns:
    pandas.DataFrame: The DataFrame with formatted column names.
    """

    # Convert all column names to snake_case
    df.columns = [''.join(['_'+i.lower() if i.isupper() else i for i in col]).lstrip('_') for col in df.columns]

    # Remove spaces from column names
    df.columns = df.columns.str.replace(' ', '')

    # Rename specific columns if necessary
    df = df.rename(columns={'object_i_d': 'object_id'})

    return df


df = format_column_names(df)


# Function to remove special characters
def remove_special_characters(text, keep_whitespace=True):
    if keep_whitespace:
        return ''.join(e for e in text if e.isalnum() or e.isspace())
    else:
        return ''.join(e for e in text if e.isalnum())

# Applying the function to the DataFrame columns
df['object_name'] = df['object_name'].apply(remove_special_characters)
df['title'] = df['title'].apply(remove_special_characters)


#Function to create primary keys (unique identifiers for dimension tables)
def create_id_column(existing_column, id_column):
    # Create a dictionary to store the mapping of existing_column to IDs
    id_mapping = {'unknown': 0}

    # Auto-incrementing counter for assigning IDs
    id_counter = 1

    # Iterate through unique values in existing_column and assign IDs
    for value in existing_column.dropna().unique():
        if pd.notna(value) and value != 'unknown':
            id_mapping[value] = id_counter
            id_counter += 1

    # Map the IDs back to the DataFrame
    id_column_values = existing_column.map(id_mapping)

    # Fill NaN values in id_column with 0
    id_column_values.fillna(0, inplace=True)

    # Convert id_column to integer
    id_column_values = id_column_values.astype(int)

    return id_column_values


#Add IDs
df['artist_id'] = create_id_column(df['artist_display_name'], 'artist_id')
df['artist_display_name'].fillna('Unknown', inplace=True)

df['geography_id'] = create_id_column(df['geography_type'], 'geography_id')
df['geography_type'].fillna('Unknown', inplace=True)

df['period_id'] = create_id_column(df['period'], 'period_id')
df['period'].fillna('Unknown', inplace=True)

df['department_id'] = create_id_column(df['department'], 'department_id')
df['department'].fillna('Unknown', inplace=True)

df['credit_line_id'] = create_id_column(df['credit_line'], 'credit_line_id')
df['credit_line'].fillna('Unknown', inplace=True)

df['region_id'] = create_id_column(df['region'], 'region_id')
df['region'].fillna('Unknown', inplace=True)


#For generating location id
unique_values = df[['city', 'state', 'county', 'country']].drop_duplicates()
unique_values['location_id'] = range(0, len(unique_values) )

merged_df = pd.merge(df, unique_values, on=['city', 'state', 'county', 'country'], how='left')


#Export as csv
merged_df.to_csv('cleaned_data_with_ids.csv',index=0)



