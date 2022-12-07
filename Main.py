import time
import os

import src.data.extract_data as ed # extracting data
import src.data.transform_data as td # transforming data
import src.visualization.visualize as v # creating visualizations

# -----------------------------------------------------------------------------
# Creating relevant folders and folders variables
# -----------------------------------------------------------------------------

# Defining project folder as our main directory
dirname = os.getcwd() 

# location folders variables
data_raw = dirname + "\\data\\raw\\"
data_interim = dirname + "\\data\\interim\\"
data_processed = dirname + "\\data\\processed\\"
figures = dirname + "\\reports\\figures\\"

# creating list of paths to loop through
folders = [data_raw, 
            data_interim, 
            data_processed,
            figures
            ]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        with open(folder + '.gitkeep', 'w') as fp: # create .gitkeep file
            pass
        print(f"Directory Created:{folder}\n")

wait = input("Press Enter to continue.")

# -----------------------------------------------------------------------------
# Scraping data
# -----------------------------------------------------------------------------

# specifying variables input for searching
job_title = str(input("job_title: "))
location = str(input("location: "))

# 
job_links = ed.scrape_linkedin_search_page(job_title, location)
wait = input("Press Enter to continue.")

words_str = ed.scrape_linkedin_offers(job_links)
wait = input("Press Enter to continue.")

df_words = ed.create_count_words_df(words_str)
wait = input("Press Enter to continue.")

#generating a raw csv file
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
df_words.to_csv(data_raw + file_name, index=False)
print("raw data saved")
wait = input("Press Enter to continue.")

# -----------------------------------------------------------------------------
# Filtering data from non useful words
# -----------------------------------------------------------------------------
td.stopwords(path_from=data_raw, path_to=data_interim)
wait = input("Press Enter to continue.")
# -----------------------------------------------------------------------------
# Populating most in-demand programming languages from job search
# -----------------------------------------------------------------------------
programming_languages = td.populate_programming_languages()
td.filter_for_list_of_words(path_from=data_interim, 
                            path_to=data_processed,
                            f_name="languages_",
                            search_for=programming_languages)
wait = input("Press Enter to continue.")
# -----------------------------------------------------------------------------
# Populating most in-demand BI tools from job search
# -----------------------------------------------------------------------------

# Here I will be using a custom list I've made:
tools = [
    "excel",
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
    "graylog",
]

td.filter_for_list_of_words(path_from=data_interim, 
                            path_to=data_processed,
                            f_name="BI-tools_",
                            search_for=tools)
wait = input("Press Enter to continue.")




tools = [
    "gcp",
    "google",
    "aws",
    "amazon",
    "google",
    "azure",
    "microsoft",
    "alibaba",
    "oracle",
    "ibm",
    "kyndryl",
    "rackspace",
    "salesforce",
    "sap",
    "ovh",
    "digitalocean",
    "tencent",
    "vmware"
]

td.filter_for_list_of_words(path_from=data_interim, 
                            path_to=data_processed,
                            f_name="Cloud_",
                            search_for=tools)
wait = input("Press Enter to continue.")

# -----------------------------------------------------------------------------
# Generating word clouds and bar charts
# -----------------------------------------------------------------------------
v.generate_wordcloud(path_from=data_interim, path_to=figures)
wait = input("Press Enter to continue.")

v.generate_bar_charts(path_from=data_processed, path_to=figures)
wait = input("Press Enter to continue.")

