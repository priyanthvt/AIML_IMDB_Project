import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

selected_page = st.sidebar.selectbox('Select an option', ['Top 10 Movies by Rating and Voting Counts', 'Genre Distribution',
                                                        'Average Duration by Genre', 'Voting Trends by Genre',
                                                        'Rating Distribution', 'Genre-Based Rating Leaders',
                                                        'Most Popular Genres by Voting', 'Duration Extremes',
                                                        'Ratings by Genre', 'Correlation Analysis',
                                                        'Interactive Filtering Functionality'])

st.markdown(f'**{selected_page}**')

conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='pwd12345',
        database='practice'
    )

cursor = conn.cursor()

if selected_page == 'Top 10 Movies by Rating and Voting Counts':
    cursor.execute("""SELECT MOVIE_NAME, RATING, VOTING_COUNT FROM
    (SELECT *, ROW_NUMBER() OVER (PARTITION BY MOVIE_NAME ORDER BY RATING DESC, VOTING_COUNT DESC) AS RN FROM IMDB_MOVIES
    WHERE VOTING_COUNT > (SELECT AVG(VOTING_COUNT) FROM IMDB_MOVIES))
    AS RANKED
    WHERE RN = 1
    ORDER BY RATING DESC, VOTING_COUNT DESC
    LIMIT 10""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Movie_name', 'Rating', 'Voting_Count'])

    st.dataframe(df)

elif (selected_page == 'Genre Distribution'):
    st.write('Count of movies for each genre')
    cursor.execute("""SELECT GENRE, COUNT(MOVIE_NAME) AS NO_OF_MOVIES FROM IMDB_MOVIES
                                GROUP BY GENRE""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Genre', 'Movies_Count'])

    fig, ax = plt.subplots()
    bar_chart = ax.bar(df['Genre'], df['Movies_Count'])
    ax.set_xlabel('Genre')
    ax.set_ylabel('Movies Count')
    ax.bar_label(bar_chart)
    st.pyplot(fig)

elif (selected_page == 'Average Duration by Genre'):
    st.write('Average movie duration per genre')
    cursor.execute("""SELECT GENRE, ROUND(AVG(DURATION_IN_MINS)) AS AVERAGE_MOVIE_DURATION FROM IMDB_MOVIES
                        GROUP BY GENRE""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Genre', 'Average_Movie_Duration'])
    fig, ax = plt.subplots()
    barh_chart = ax.barh(df['Genre'], df['Average_Movie_Duration'])
    ax.set_xlabel('Average Movie Duration [in mins]')
    ax.set_ylabel('Genre')
    ax.bar_label(barh_chart)
    st.pyplot(fig)

elif (selected_page == 'Voting Trends by Genre'):
    cursor.execute("""SELECT GENRE, ROUND(AVG(Voting_Count)) AS AVERAGE_VOTING_COUNT FROM IMDB_MOVIES
                        GROUP BY GENRE""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Genre', 'Average_Voting_Counts'])

    fig, ax = plt.subplots()
    ax.plot(df['Genre'], df['Average_Voting_Counts'], marker='o', color='green')
    ax.set_xlabel('Genre')
    ax.set_ylabel('Average Voting Counts')
    ax.set_title('Voting Trends by Genre')
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif (selected_page == 'Rating Distribution'):
    cursor.execute("""SELECT MOVIE_NAME, RATING FROM IMDB_MOVIES""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Movie_Name', 'Rating'])
    fig, ax = plt.subplots()
    ax.hist(df['Rating'], color = 'skyblue', edgecolor = 'green')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Movies Count')
    ax.set_title('Rating Distribution')
    st.pyplot(fig)

elif (selected_page == 'Genre-Based Rating Leaders'):
    st.write('Top-rated movies for each genre')
    cursor.execute("""SELECT MOVIE_NAME, GENRE, RATING FROM
                        (SELECT *, DENSE_RANK() OVER (PARTITION BY GENRE ORDER BY RATING DESC) AS RN FROM IMDB_MOVIES) AS MOVIES
                            WHERE RN = 1""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Movie_Name', 'Genre', 'Rating'])
    st.dataframe(df)

elif (selected_page == 'Most Popular Genres by Voting'):
    cursor.execute("""SELECT GENRE, COUNT(MOVIE_NAME) FROM IMDB_MOVIES
                        GROUP BY GENRE""")

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns = ['Genre', 'Movie_Count'])

    fig, ax = plt.subplots()
    ax.pie(df['Movie_Count'], labels = df['Genre'], autopct = '%1.2f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

elif (selected_page == 'Duration Extremes'):
    cursor.execute("""SELECT MOVIE_NAME, DURATION_IN_MINS FROM IMDB_MOVIES
                        ORDER BY DURATION_IN_MINS ASC
                            LIMIT 1""")

    shortest_movie = cursor.fetchone()

    cursor.execute("""SELECT MOVIE_NAME, DURATION_IN_MINS FROM IMDB_MOVIES
                        ORDER BY DURATION_IN_MINS DESC
                            LIMIT 1""")

    longest_movie = cursor.fetchone()

    movie = {
        'Movie_Name' : [shortest_movie[0], longest_movie[0]],
        'Duration_in_mins' : [shortest_movie[1], longest_movie[1]]
    }

    df = pd.DataFrame(movie, index = ['shortest', 'longest'])
    st.dataframe(df)

elif (selected_page == 'Ratings by Genre'):
    cursor.execute("""SELECT GENRE, ROUND(AVG(RATING), 1) AS AVERAGE_RATING FROM IMDB_MOVIES
                        GROUP BY GENRE""")

    genre_average_rating = cursor.fetchall()

    df = pd.DataFrame(genre_average_rating, columns = ['Genre', 'Rating'])
    df.set_index('Genre', inplace = True)
    fig, ax = plt.subplots()
    sns.heatmap(df, annot = True)
    st.pyplot(fig)

elif (selected_page == 'Correlation Analysis'):
    cursor.execute("""SELECT RATING, VOTING_COUNT FROM IMDB_MOVIES""")

    rating_voting_count = cursor.fetchall()

    df = pd.DataFrame(rating_voting_count, columns = ['Rating', 'Voting_Count'])
    fig, ax = plt.subplots()
    ax.scatter(x='Rating', y='Voting_Count', data =df)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Voting Count')
    st.pyplot(fig)

elif (selected_page == 'Interactive Filtering Functionality'):

    cursor.execute("""SELECT MAX(VOTING_COUNT) AS MAX_VOTING_COUNT FROM IMDB_MOVIES""")
    max_voting_count = cursor.fetchone()[0]

    cursor.execute("""SELECT MIN(VOTING_COUNT) AS MIN_VOTING_COUNT FROM IMDB_MOVIES""")
    min_voting_count = cursor.fetchone()[0]

    voting = st.slider("Voting", min_value = min_voting_count, max_value = max_voting_count, step = 1000)

    where_condition = 'WHERE'
    where_condition += f' VOTING_COUNT > {voting}'

    cursor.execute("""SELECT DISTINCT GENRE FROM IMDB_MOVIES""")
    movie_genres = cursor.fetchall()
    genres = [g[0] for g in movie_genres]

    genre = st.selectbox('Select the genre : ', [None] + genres)

    if genre is not None:
        where_condition += ' AND GENRE' + ' = ' + '\'' + genre + '\''

    cursor.execute("""SELECT MIN(RATING) FROM IMDB_MOVIES""")
    min_rating = cursor.fetchone()[0]

    cursor.execute("""SELECT MAX(RATING) FROM IMDB_MOVIES""")
    max_rating = cursor.fetchone()[0]

    rating = st.slider("Rating", min_value = min_rating, max_value = max_rating, step = 0.1)

    where_condition += f' AND RATING > {rating}'

    duration = st.radio('Movie Duration : ', ('All', '< 1 hr', '1 - 2 hrs', '2 - 3 hrs', r'\> 3 hrs'))

    if duration == '< 1 hr':
        where_condition += ' AND DURATION_IN_MINS < 60'
    elif duration == '1 - 2 hrs':
        where_condition += ' AND DURATION_IN_MINS BETWEEN 60 AND 120'
    elif duration == '2 - 3 hrs':
        where_condition += ' AND DURATION_IN_MINS BETWEEN 120 AND 180'
    elif duration == r'\> 3 hrs':
        where_condition += ' AND DURATION_IN_MINS > 180'

    select_query = 'SELECT * FROM IMDB_MOVIES'

    db_query = select_query + ' ' + where_condition
    st.write(db_query)

    cursor.execute(db_query)

    movies = cursor.fetchall()

    df = pd.DataFrame(movies, columns = ['Movie_Name', 'Genre', 'Rating', 'Voting Count', 'Duration_In_Mins'])

    st.dataframe(df)

cursor.close()
conn.close()

