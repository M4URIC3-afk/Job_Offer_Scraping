from wordcloud import WordCloud  # generates word clouds 
import matplotlib.pyplot as plt  # creates visualizations 
import seaborn as sns # creates visualizations
import pandas as pd

import os

# -----------------------------------------------------------------------------
# plotting word cloud
# -----------------------------------------------------------------------------
def generate_wordcloud(path_from, path_to):
    # selecting csv
    files_of_interest = []
    for f in os.listdir(path_from):
        if f.endswith("csv"):
            files_of_interest.append(path_from + f)
    latest_file = max(files_of_interest, key=os.path.getctime)
    # creating dict of words
    df = pd.read_csv(latest_file)
    words_dict = pd.Series(df['word_count'].values,index=df['word']).to_dict()
    # generating wordcloud object
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color="white",
        min_font_size=10
        ).generate_from_frequencies(words_dict)
    # plotting the WordCloud image with matplotlib
    plt.figure(figsize=(8, 8), facecolor="black")
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    # printing the plot
    plt.show()
    # saving the plot
    file_name = os.path.basename(latest_file)
    wordcloud.to_file(path_to + file_name + '.png')
    print(f'Wordcloud saved in {path_to}')
    

# -----------------------------------------------------------------------------
# Script if executed on its own
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    generate_wordcloud(path_from="../../data/interim", path_to="../../reports/figures")