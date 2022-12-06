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
        
    soup_programming_languages = BeautifulSoup(programming_languages_page.text, features='lxml')
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
        "portable",
        "carbon",
        "gap",
        "actor"
    ]
    langs.difference_update(removelist)
    print(f"Programming languages populated: {len(langs)}")
    
    return langs


# -----------------------------------------------------------------------------
# Returns most in-demand programming languages
# -----------------------------------------------------------------------------
def filter_for_list_of_words(path_from, path_to, search_for, f_name):
    # listing files from dir
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    # keeping only the programming languages from the df_word   
    for f in files_of_interest:
        df = pd.read_csv(f)
        df = df[df["word"].isin(search_for)]
        # # reformating the index
        # df = df.reset_index()
        # df.drop("index", axis=1)
        # saving as csv
        file_name = os.path.basename(f)
        df.to_csv(path_to + f_name + file_name, index=False)
        print(f"filter applied to file {file_name}")
        

# -----------------------------------------------------------------------------
# Script if executed on its own
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    stopwords(path_from="../../data/raw/", path_to="../../data/interim/")
    
    progamming_languages = populate_programming_languages()
    filter_for_list_of_words(path_from="../../data/raw/", 
                            path_to="../../data/interim/",
                            f_name="languages_",
                            search_for=progamming_languages)
    
    tools = [
    "power",
    "tableau",
    "cognos",
    "excel",
    "matlab",
    "qlikview",
    "splunk",
    "grafana",
    "looker",
    "domo",
    "dundas",
    "yellowfin",
    "zoho",
    "plotly",
    "kibana",
    "graphite",
    "graylog"
    ]
    
    filter_for_list_of_words(path_from="../../data/interim/", 
                            path_to="../../data/processed/",
                            f_name="BI-tools_",
                            search_for=tools)