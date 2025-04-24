from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

driver = webdriver.Chrome()

genre_list = ['Adventure', 'Animation', 'Biography', 'Family', 'Fantasy']

for genre in genre_list:

    title_list = []
    ratings_list = []
    voting_count_list = []
    duration_list = []

    driver.get('https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31')
    wait = WebDriverWait(driver, 10)

    genre_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[.//div[text()='Genre']]")))
    driver.execute_script("arguments[0].click();", genre_button)

    genre_Type_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[.//span[text() = '{genre}']]")))
    driver.execute_script("arguments[0].click();", genre_Type_button)

    current_movie_count = 0

    while True:
        movie_details = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[class = "sc-5179a348-0 kfocva"]')))
        new_movies = movie_details[current_movie_count:]

        for movie in new_movies:
            try:
                title_element = movie.find_element(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper h3.ipc-title__text')
                title_list.append(title_element.text)
            except:
                title_list.append(None)

            try:
                rating_element = movie.find_element(By.XPATH, './/span[@class = "ipc-rating-star--rating"]')
                ratings_list.append(rating_element.text)
            except:
                ratings_list.append(None)

            try:
                vote_count_element = movie.find_element(By.XPATH, './/span[@class = "ipc-rating-star--voteCount"]')
                voting_count_list.append(vote_count_element.text)
            except:
                voting_count_list.append(None)

            try:
                duration_element = movie.find_element(By.XPATH,'.//span[contains(@class, "dli-title-metadata-item") and (contains(text(), "h") or contains(text(), "m"))]')
                duration_list.append(duration_element.text)
            except:
                duration_list.append(None)

        current_movie_count = len(title_list)

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ipc-see-more__text']")))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
        except Exception as e:
            print("No more pages")
            break

    df = pd.DataFrame({
        'Movie_Name' : title_list,
        'Rating' : ratings_list,
        'Voting_Count' : voting_count_list,
        'Duration_in_mins' : duration_list
    })

    df.insert(1, 'Genre', genre)

    print(df)

    csv_file_name = genre + ' Movies.csv'

    df.to_csv(os.path.join(r'C:\Users\Sheasaanth\Desktop\Priyanth\IMDB_Project\DataScrapping\Dataset\\', csv_file_name), index=False)
    print('IMDB data scrapped')
driver.quit()