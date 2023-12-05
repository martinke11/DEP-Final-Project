#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 11:01:43 2023

@author: katherinemartin
"""
import pandas as pd
import pycountry
import os
os.chdir('/Users/katherinemartin/Desktop/Autumn 2023/Data Engineering /Final Project')

df = pd.read_csv('MetObjects.csv')


columns_to_drop = ['Object Number', 'Gallery Number', 'Portfolio', 'Artist Prefix', 'Artist Display Bio',
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

df['AccessionYear'] = pd.to_datetime(df['AccessionYear'], errors='coerce').dt.year
df['AccessionYear'] = df['AccessionYear'].fillna(0).astype(int)

df.rename(columns={'Artist Gender': 'Is Female'}, inplace=True)
df['Is Female'] = df['Is Female'].apply(lambda x: 1 if x else 0)

# Artist Role
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
    
df['Artist Begin Date'] = pd.to_datetime(df['Artist Begin Date'], errors='coerce').dt.year
df['Artist End Date'] = pd.to_datetime(df['Artist End Date'], errors='coerce').dt.year

df['Artist Begin Date'] = df['Artist Begin Date'].fillna(0).astype(int)
df['Artist End Date'] = df['Artist End Date'].fillna(0).astype(int)

## Assumed that the Nationality data is filled according to country naming conventions
df['Artist Nationality'] = df['Artist Nationality'].str.split('|').str[0].str.strip()
df['Artist Nationality'] = df['Artist Nationality'].str.capitalize()

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

df['Constituent ID'] = pd.to_numeric(df['Constituent ID'], errors='coerce').fillna(0).astype(int)

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

def to_snake_case(name):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in name]).lstrip('_')

# Convert all column names to snake_case
df.columns = [to_snake_case(col) for col in df.columns]

df.columns = df.columns.str.replace(' ', '')
df = df.rename(columns={'constituent_i_d': 'constituent_id'})
df = df.rename(columns={'object_i_d': 'object_id'})

# Function to remove special characters
def remove_special_characters(text, keep_whitespace=True):
    if keep_whitespace:
        return ''.join(e for e in text if e.isalnum() or e.isspace())
    else:
        return ''.join(e for e in text if e.isalnum())

# Applying the function to the DataFrame columns
df['object_name'] = df['object_name'].apply(remove_special_characters)
df['title'] = df['title'].apply(remove_special_characters)

df.head()
df.dtypes
df.to_csv('cleaned_data.csv')
