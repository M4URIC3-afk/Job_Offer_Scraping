import pandas as pd
import advertools as adv  # provides options for text analysis
import requests
from bs4 import BeautifulSoup  # makes it easy to scrape information from web pages


import os

# -----------------------------------------------------------------------------
#  Filer words
# -----------------------------------------------------------------------------
def stopwords(path_from, path_to):
    """Go through a series of csv files countaining words count to apply a filter and return csv files without those words

    Args:
        path_from (str): folder from
        path_to (str): folder to
    """
    # listing files from dir
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    # merging files into one dataframe
    sw_en_fr = (
        adv.stopwords["english"]
        .union(adv.stopwords["french"])
        .union(
            {"d", "l", ":", "&", "/", "êtes", "2", "avez", "d'une", "!", "-", "?", "1"}
        )
    )
    for f in files_of_interest:
        df = pd.read_csv(f)
        df = df[~df["word"].isin(sw_en_fr)]
        print(f"filers applied")
        file_name = os.path.basename(f)
        df.to_csv(path_to + file_name, index=False)
        print(f"word's filter applied to file {file_name}")


# -----------------------------------------------------------------------------
# Populating programming languages list
# -----------------------------------------------------------------------------
def populate_programming_languages():
    """Scrape wikipedia to get a list of programming languages

    Returns:
        list: List of programming languages
    """
    # Using wikipedia page to make sure we stay up to date with programming languages
    programming_languages_page = requests.get(
        "http://en.wikipedia.org/wiki/List_of_programming_languages"
    )
    # Ensuring the get request is successful
    if programming_languages_page: # if we use a requests.models.Response instance in a conditional expression, it evaluates to True if the status code is between 200 and 400, and False otherwise
        print("Wikipedia page http://en.wikipedia.org/wiki/List_of_programming_languages available for scraping.")
    else:
        print("Wikipedia page http://en.wikipedia.org/wiki/List_of_programming_languages not available.")
        
    soup_programming_languages = BeautifulSoup(programming_languages_page.text)
    langs = []
    # parse all the links.
    for link in soup_programming_languages.find_all("a"):
        # making it break on the Last link after Z++ which is "List of programming languages"
        if link.get_text() == "List of programming languages":
            break
        if link.get_text() == "edit":
            pass
        else:
            langs.append(link.get_text())

    # find u'See also'
    see_also_index_ = langs.index("See also")
    # strip out headers
    langs = langs[see_also_index_ + 1 :]
    # convert list to lower-case
    langs = [lang.lower() for lang in langs]
    # converting list to set
    langs = set(langs)
    # removing languages with ambiguous names or the ones that I'm collecting by mistake (alphabet links etc.)
    removelist = [
        "plus",
        "es",
        "d",
        "help",
        "media",
        "go",
        "claire",
        "simple",
        "category",
        "b",
        "clean",
        "français",
        "source",
        "e",
        "toi",
        "beta",
        "small",
        "developers",
        "focus",
        "joy",
        "processing",
        "resources",
        "contributions",
        "reason",
        "rapid",
        "hope",
        "scratch",
        "self",
        "pilot",
        "ml",
        "pipelines",
        "dc",
        "abc",
        "inform",
        "ease",
        "basic",
        "lean",
        "skill",
        "read",
        "statistics",
        "tea",
        "dog",
        "definitions",
        "logo",
        "history",
        "talk",
        "mad",
        "chill",
        "s",
        "t",
        "hack",
        "cool",
    ]
    langs.difference_update(removelist)
    print(f"Programming languages populated: {len(langs)}")
    
    return langs
# -----------------------------------------------------------------------------
# Merging csv into one working file
# -----------------------------------------------------------------------------
# def process_data(path_from):
#     """"""
#     # listing files from dir
#     files_in_dir = []
#     for f in os.listdir(path_from):
#         if f.endswith("csv"):
#             files_in_dir.append(path_from + f)
#     print(f'files in dir: {files_in_dir}')
#     # merging files into one dataframe
#     df = pd.concat((pd.read_csv(f) for f in files_in_dir), ignore_index=True)
#     print(df.head())
#     return df


