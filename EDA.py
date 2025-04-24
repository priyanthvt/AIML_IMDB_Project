import pandas as pd
import re
import os

movies_df = pd.read_csv(r'C:\Users\Sheasaanth\Desktop\Priyanth\IMDB_Project\DataScrapping\Dataset\Movies.csv')

movies_cleaned = movies_df.copy()

movies_cleaned['Movie_Name'] = movies_cleaned['Movie_Name'].apply(lambda x : re.sub(r'^\d+\.\s','',x.strip()).strip() if isinstance(x, str) else x)

movies_cleaned['Voting_Count'] = movies_cleaned['Voting_Count'].apply(
    lambda x : int(float(re.sub(r'k', '', x.strip(' ').replace('(', '').replace(')', '').strip(), flags = re.IGNORECASE)) * 1000)
    if isinstance(x, str) and re.search(r'k', x, re.IGNORECASE)
    else int(x.strip(' ').replace('(', '').replace(')', '').strip())
    if isinstance(x, str)
    else 0
    if pd.isnull(x)
    else x)

def convert_to_minutes(movie_duration):
    if isinstance(movie_duration, str):
        movie_duration = movie_duration.strip().lower()

        if 'h' in movie_duration and 'm' in movie_duration:
            movie_duration = movie_duration.replace('h', '').replace('m', '').strip()
            hour, minute = movie_duration.split()
            return int((int(hour) * 60) + int(minute))

        elif 'h' in movie_duration:
            movie_duration = movie_duration.replace('h', '').strip()
            return int(movie_duration) * 60

        elif 'm' in movie_duration:
            movie_duration = movie_duration.replace('m', '').strip()
            return int(movie_duration)

    return movie_duration

movies_cleaned['Duration_in_mins'] = movies_cleaned['Duration_in_mins'].apply(lambda x : convert_to_minutes(x))

movies_cleaned['Rating'] = movies_cleaned['Rating'].fillna(0)
movies_cleaned['Duration_in_mins'] = movies_cleaned['Duration_in_mins'].fillna(int(movies_cleaned['Duration_in_mins'].mean()))
movies_cleaned['Duration_in_mins'] = movies_cleaned['Duration_in_mins'].astype(int)

movies_cleaned.to_csv(os.path.join(r'C:\Users\Sheasaanth\Desktop\Priyanth\IMDB_Project\DataScrapping\Dataset\\', 'Movies Cleaned Dataset.csv'), index=False)

print('File saved')