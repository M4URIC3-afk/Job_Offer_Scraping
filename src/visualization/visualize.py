from wordcloud import WordCloud  # generates word clouds
import matplotlib.pyplot as plt  # creates visualizations
import seaborn as sns  # creates visualizations
import pandas as pd

import os

# -----------------------------------------------------------------------------
# plotting word cloud
# -----------------------------------------------------------------------------
def generate_wordcloud(path_from, path_to):
    """Generate a wordcloud from csv files saved in a given folder. CSV files need to be formated with column 'word' with all the given words and column 'word_count' with the weight of each word

    Args:
        path_from (str): path from where to look for csv
        path_to (str): path from where to save  wordcloud png file
    """
    # selecting csv
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    #latest_file = max(files_of_interest, key=os.path.getctime)
    # creating dict of words
    for f in files_of_interest:
        df = pd.read_csv(f)
        words_dict = pd.Series(df["word_count"].values, index=df["word"]).to_dict()
    # generating wordcloud object
        wordcloud = WordCloud(
            width=800, height=800, background_color="white", min_font_size=10
    ).generate_from_frequencies(words_dict)
        # plotting the WordCloud image with matplotlib
        plt.figure(figsize=(8, 8), facecolor="black")
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        # printing the plot
        # plt.show()
        # saving the plot
        file_name = os.path.basename(f)
        wordcloud.to_file(path_to + file_name + ".png")
        print(f"Wordcloud {file_name} saved in {path_to}")

# -----------------------------------------------------------------------------
#  plotting bar charts
# -----------------------------------------------------------------------------
def generate_bar_charts(path_from, path_to):
    # selecting csv
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    for f in files_of_interest:
        df = pd.read_csv(f)
        file_name = os.path.basename(f)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data = df, 
                    x = 'word',
                    y = 'word_count',
                    ax=ax
                    ).set(title=file_name)
        plt.savefig(path_to + file_name + '.png')


# -----------------------------------------------------------------------------
# Script if executed on its own
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    generate_wordcloud(path_from="../../data/interim", path_to="../../reports/figures")
    generate_bar_charts(path_from="../../data/processed", path_to="../../reports/figures")
