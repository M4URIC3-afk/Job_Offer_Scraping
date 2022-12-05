import pandas as pd
import advertools as adv  # provides options for text analysis

import os

# -----------------------------------------------------------------------------
#  Filer words
# -----------------------------------------------------------------------------
def stopwords(path_from, path_to):
    # listing files from dir
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    # merging files into one dataframe
    sw_en_fr = adv.stopwords["english"].union(adv.stopwords["french"]).union({
        "d", 
        "l",
        ":",
        "&",
        "/",
        "êtes",
        "2",
        "avez",
        "d'une",
        "!",
        "-",
        "?",
        "1"
        })
    for f in files_of_interest:
        df = pd.read_csv(f)
        df = df[~df['word'].isin(sw_en_fr)]
        print(f'filers applied')
        file_name = os.path.basename(f)
        df.to_csv(path_to + file_name, index=False)
        print(f"word's filter applied to file {file_name}")


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