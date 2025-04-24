import pandas as pd
import os

folder_path = r'C:\Users\Sheasaanth\Desktop\Priyanth\IMDB_Project\DataScrapping\Dataset'

file_list = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
df_list = []

for file in file_list:
    df = pd.read_csv(os.path.join(folder_path, file))
    df_list.append(df)

movies_df = pd.concat(df_list, ignore_index = True)

movies_df.to_csv(os.path.join(folder_path, 'Movies.csv'), index=False)

print('csv files merged')


