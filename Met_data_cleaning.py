#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import pycountry
import os
os.chdir('/Users/mitalidighe/Desktop/UChicago Quarter 1/DEP/Final project/MoMA/Final Presentation')

df = pd.read_csv('MetObjects.csv')


# In[ ]:


# deleted 'Constinuent ID' because it wasnt unique and created a unique key using a function

columns_to_drop = ['Constituent ID', 'Object Number', 'Gallery Number', 'Portfolio', 'Artist Prefix', 'Artist Display Bio',
                   'Artist Suffix', 'Artist Alpha Sort', 'Artist ULAN URL', 'Artist Wikidata URL', 'Object Date',
                   'Classification', 'Rights and Reproduction', 'Link Resource', 'Object Wikidata URL',
                   'Metadata Date', 'Repository', 'Tags', 'Tags AAT URL', 'Tags Wikidata URL']
df.drop(columns=columns_to_drop, inplace=True)

# Dropping rows with no Title, and other redundant column values
df.dropna(subset=['Title'], inplace=True)
df.dropna(subset=['AccessionYear'], inplace=True)
df.dropna(subset=['Object Name'], inplace=True)
df.dropna(subset=['Medium'], inplace=True)
df.dropna(subset=['Credit Line'], inplace=True)
df.dropna(subset=['Dimensions'], inplace=True)

df.isna().sum()


# In[ ]:


#Change datatype to year
df['AccessionYear'] = pd.to_datetime(df['AccessionYear'], errors='coerce').dt.year
df['AccessionYear'] = df['AccessionYear'].fillna(0).astype(int)

#Artist gender - is female flag
df.rename(columns={'Artist Gender': 'Is Female'}, inplace=True)
df['Is Female'] = df['Is Female'].apply(lambda x: 0 if pd.isnull(x) else 1)

# Artist Role cleaning
df['Artist Role'] = df['Artist Role'].str.split('|').str[0]

columns_to_convert = ['Is Highlight', 'Is Timeline Work', 'Is Public Domain']

for col in columns_to_convert:
    df[col] = df[col].apply(lambda x: 0 if x == False else 1)
    
string_columns = [
    "Culture", "Period", "Dynasty", "Reign", 
    "Artist Role", "Artist Display Name", "City", "State", 
    "County", "Country", "Region", "Subregion", 
    "Locale", "Locus", "Excavation", "River"
]

for col in string_columns:
    df[col] = df[col].str.strip()
    df[col] = df[col].replace('', 'Unknown')
    df[col] = df[col].replace('nan', 'Unknown')
    df[col] = df[col].fillna('Unknown')


# In[ ]:


#Change data types
df['Artist Begin Date'] = pd.to_datetime(df['Artist Begin Date'], errors='coerce').dt.year
df['Artist End Date'] = pd.to_datetime(df['Artist End Date'], errors='coerce').dt.year

df['Artist Begin Date'] = df['Artist Begin Date'].fillna(0).astype(int)
df['Artist End Date'] = df['Artist End Date'].fillna(0).astype(int)

## Assumed that the Nationality data is filled according to country naming conventions
df['Artist Nationality'] = df['Artist Nationality'].str.split('|').str[0].str.strip()
df['Artist Nationality'] = df['Artist Nationality'].str.capitalize()


# In[ ]:


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

# Geography cleaning
df['geography_type'] = df['geography_type'].str.split('|').str[0]
df['geography_type'].fillna('Unknown', inplace=True)


# In[ ]:


# Checking all the string columns for absurd values
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna('Unknown')  # Replace NaN with 'Unknown'
    df[col] = df[col].str.strip()        # Strip white spaces
    df[col] = df[col].apply(lambda x: 'Unknown' if not x.isascii() or x.isnumeric() else x)
    
# Normalizing Text Data
string_columns = df.select_dtypes(include='object').columns
df[string_columns] = df[string_columns].apply(lambda x: x.str.lower())

# Checking for Duplicates
before_removal = df.shape[0]
df = df.drop_duplicates()
after_removal = df.shape[0]


# In[ ]:


def to_snake_case(name):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in name]).lstrip('_')

# Convert all column names to snake_case
df.columns = [to_snake_case(col) for col in df.columns]

df.columns = df.columns.str.replace(' ', '')
df = df.rename(columns={'object_i_d': 'object_id'})


# In[ ]:


# Function to remove special characters
def remove_special_characters(text, keep_whitespace=True):
    if keep_whitespace:
        return ''.join(e for e in text if e.isalnum() or e.isspace())
    else:
        return ''.join(e for e in text if e.isalnum())

# Applying the function to the DataFrame columns
df['object_name'] = df['object_name'].apply(remove_special_characters)
df['title'] = df['title'].apply(remove_special_characters)


# In[ ]:


df.dtypes


# In[ ]:


df.shape


# In[ ]:


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


# In[ ]:


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


# In[ ]:


#For generating location id

unique_values = df[['city', 'state', 'county', 'country']].drop_duplicates()
unique_values['location_id'] = range(0, len(unique_values) )

merged_df = pd.merge(df, unique_values, on=['city', 'state', 'county', 'country'], how='left')


# In[ ]:


merged_df.shape


# In[ ]:


#Export as csv
merged_df.to_csv('cleaned_data_with_ids.csv',index=0)


# In[ ]:


#Code to import csv to met database

import pandas as pd
from sqlalchemy import create_engine

# MySQL connection string
# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your MySQL credentials
connection_string = "mysql+pymysql://root:rootroot@127.0.0.1:3306/met"

#Change CSV file path according to working directory
csv_file_path = '/Users/mitalidighe/Desktop/UChicago Quarter 1/DEP/Final project/MoMA/Final Presentation/cleaned_data_with_ids.csv'

# Table name in MySQL
table_name = 'cleaned_data_with_ids'

# Read CSV file into a pandas DataFrame
df_2 = pd.read_csv(csv_file_path)

# Create a MySQL connection and upload the DataFrame to the table
engine = create_engine(connection_string)
df_2.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Close the MySQL connection
engine.dispose()

