from sqlalchemy import create_engine
import pandas as pd

movies_cleaned_df = pd.read_csv(r'C:\Users\Sheasaanth\Desktop\Priyanth\IMDB_Project\DataScrapping\Dataset\Movies Cleaned Dataset.csv')

username = 'root'
password = 'pwd12345'
host = 'localhost'
port = 3306
database = 'practice'

connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(connection_string)

connection = engine.connect()

movies_cleaned_df.to_sql(name='IMDB_MOVIES', con=engine, if_exists='replace', index=False)

print('DF saved in DB')

connection.close()