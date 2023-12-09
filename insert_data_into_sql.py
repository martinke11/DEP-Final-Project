from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd 
import os
os.chdir('/Users/katherinemartin/Desktop/Autumn 2023/Data Engineering /Final Project')


#Code to import csv to met database
# MySQL connection string
# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your MySQL credentials
connection_string = "mysql+pymysql://root:rootroot@127.0.0.1:3306/met"

#Change CSV file path according to working directory
csv_file = 'cleaned_data_with_ids.csv'

# Table name in MySQL
table_name = 'cleaned_data_with_ids'

# Read CSV file into a pandas DataFrame
df_2 = pd.read_csv(csv_file)

# Create a MySQL connection and upload the DataFrame to the table
engine = create_engine(connection_string)
df_2.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Close the MySQL connection
engine.dispose()