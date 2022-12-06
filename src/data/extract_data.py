from selenium import webdriver  # automates web browser interaction
from bs4 import BeautifulSoup  # makes it easy to scrape information from web pages
import requests  # makes HTTP requests
import pandas as pd

import time  # provides various time-related functions
import random  # implements pseudo-random number generators
from collections import (
    Counter,
)  # provides specialized container datatypes - here a dict subclass for counting hashable objects

# -----------------------------------------------------------------------------
# Scraping main linkedin page
# -----------------------------------------------------------------------------
def scrape_linkedin_search_page(job_title, location):
    """Scrape linkedin job search page to extract all job offers urls from the first page for a given job title and location. Works with Firefox.

    Args:
        job_title (str): job title
        location (str): location

    Returns:
        list: list of 175 job offers urls
    """
    # transforming the inputs to a valid format for the url
    job_title_key = "%20".join(job_title.split(" "))
    location_key = "%20".join(location.split(" "))
    # generating the initial linkedin url
    url = f"https://www.linkedin.com/jobs/search?keywords={job_title_key}&location={location_key}"
    print(url)

    # Web scrapper for infinite scrolling page
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = (
        2  # You can set your own pause time. My laptop is a bit slow so I use 2 sec
    )
    screen_height = driver.execute_script(
        "return window.screen.height;"
    )  # get the screen height
    print(f"screen height: {screen_height}")

    i = 1
    while True:
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(
                screen_height=screen_height, i=i
            )
        )
        i += 1
        print("extracting urls...")
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    # creating soup object
    soup = BeautifulSoup(driver.page_source, "html.parser")

    job_links = []
    # For loop that iterates over all the <li> tags
    for h in soup.findAll("li"):
        # looking for anchor tag inside the <li>tag
        a = h.find("a")
        try:
            # looking for href inside anchor tag
            if "href" in a.attrs:
                # storing the value of href in a separate variable
                link = a.get("href")
                # appending the url to the output list
                job_links.append(link)
        # if the list does not have a anchor tag or does not have a href params we pass
        except:
            pass

    print(f"Number of links extracted: {len(job_links)}")

    job_links = [link for link in job_links if "linkedin.com/jobs/" in link]
    print(f"Number of job links: {len(job_links)}")

    if len(job_links) > 150:
        print("This is the expected number of links")
    else:
        print("Warning: this is not the expected number of links")

    return job_links


# -----------------------------------------------------------------------------
# Scraping job offer urls
# -----------------------------------------------------------------------------
def scrape_linkedin_offers(url_list):
    """Scraping job offers urls to return a string containing all content

    Args:
        url_list (list): List of all linkedin job offers to scrape through

    Returns:
        str: String of all of the content scraped
    """
    # creating text string variables
    words_str = ""
    job_info_str = ""
    i = 0
    # try/except to avoid mistakes
    time.sleep(random.uniform(1.5, 3.0))
    try:
        for link in url_list:
            # for index, link in enumerate(url_list):
            # looping through the links
            req = requests.get(link)
            # taking into account non 200 responses to try again with a bigger timer
            if req:
                i += 1
                print(f"extracting text from link {i}")
            else:
                print(f"status code error: {req.status_code}")
                # time.sleep(5)
                # req = requests.get(link) # try again on the same link
            # converting to BeautifulSoup
            soup_job_offer = BeautifulSoup(req.text, features="lxml")
            # extracting job content (within a div with a specific class) and job info (within a script with a specific type)
            job_content = soup_job_offer.find(
                "div", class_="show-more-less-html__markup"
            ).text
            job_info = soup_job_offer.find(
                "script", type="application/ld+json"
            ).text  # not used
            # appending to a string and converting to lowercase
            words_str = f"{words_str} {job_content}".lower()
            job_info_str = f"{job_info_str} {job_info}".lower()  # not used
            # pausing for few seconds to avoid 'error 429 too many requests'. Also using random to be safe
            time.sleep(random.uniform(1.5, 3.0))

    except Exception as e:
        pass

    # previewing strings contents
    print(f"\nNumber of characters extracted (including spaces): {len(words_str)}")
    print(f"\nNumber of HTTP 200 (OK) responses: {i}")

    return words_str


# -----------------------------------------------------------------------------
# Creating a dataframe with counts of words
# -----------------------------------------------------------------------------
def create_count_words_df(string):
    """Creating a dataframe with counts of words

    Args:
        string (str): Text to analyse

    Returns:
        Pandas.DataFrame: Dataframe with all words as first column ('word') and words count as second column ('word_count')
    """
    # creating a list from the string we had
    words_list = string.split()

    # creating a pandas dataframe from the list, transformed to a dictionnary. I need to look into it to make something less ugly
    df_words = pd.DataFrame.from_dict([Counter(words_list)]).T

    # renaming and sorting the df
    df_words.rename(columns={0: "word_count"}, inplace=True)
    df_words.index.names = ["word"]
    df_words.reset_index(inplace=True)
    df_words.sort_values(by=["word_count"], inplace=True, ascending=False)

    return df_words


# -----------------------------------------------------------------------------
# Script if executed on its own
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    job_title = str(input("job_title: "))
    location = str(input("location: "))

    job_links = scrape_linkedin_search_page(job_title, location)
    words_str = scrape_linkedin_offers(job_links)
    df_words = create_count_words_df(words_str)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_name = (
        "words_"
        + job_title.replace(" ", "-").replace(",", "").lower()
        + "_"
        + location.replace(" ", "-").replace(",", "").lower()
        + "_"
        + timestr
        + ".csv"
    )
    df_words.to_csv("../../data/raw/" + file_name, index=False)
    print("Raw Data extracted")
