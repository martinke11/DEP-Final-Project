from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd 


def create_connection(username, password, host, dbname):
    engine_name = f"mysql://{username}:{password}@{host}/{dbname}"

    engine = create_engine(engine_name)
    try:
        connection = engine.connect() 
    except:
        raise ValueError("Connection Failed")
    
    return connection 

if __name__ == "__main__":

    # Setting the parameters
    params = {
        'username' : 'root',
        'password' : 'rootroot',
        'host'     : '127.0.0.1:3306',
        'dbname'   : 'met'
    }

    # create the connection 
    conn = create_connection(params["username"], params["password"], params["host"], params["dbname"])

    # reading csv file 
    df = pd.read_csv("cleaned_data.csv")
    print(df.head())
    df.to_sql(name="cleaned_met_data", con=conn, index=False)

    
