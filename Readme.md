# Finding the most in-demand programming languages from Job Offers
-----------
This Python script scrapes the most recent Job Offers from a 'very well-known site' for a given job title and tells what are the most in-demand programming languages based on their occurrences. 

It is currently set up for job offers written in French or English.
It is currently set up to use Mozilla Firefox as a browser in order to scroll through this 'very well-known site' search page since job offers appear while scrolling.


## Project Organization
    ├── README.md                   <- You are here.
    ├── data
    │   ├── raw                     <- Scraped data gets uploaded here in the form of csv with words count
    │   ├── interim                 <- Intermediate data after some filters were applied to raw data in order to keep relevant words only
    │   └── processed               <- Clean data with most in-demand programming languages and BI tools
    │
    ├── notebooks                   <- Draft stuff
    │    │
    ├── reports                     <- Generated reports if any
    │   └── figures                 <- Generated graphics and figures if any
    │
    ├── requirements.txt            <- The requirements file for reproducing the environment
    │
    ├── main.py                     <- Main file to run in order to execute all scripts
    │
    └── src                         <- Source code for use in this project.
        ├── data                    
        │   └── extract_data.py     <- Script to extract the data from this 'very well-known site' and generate csv files in data/raw
        │   └── transform_data.py   <- Script to transform csv files from data/raw to interim and processed files
        │
        └── visualization           
            └── visualize.py        <- Scripts to create visualizations
     

## Description
Since I'm looking for a job, I thought I should define what are the most in-demand programming languages and dashboarding tools in the job market. And could use python to do that while learning. 


## Demo video
https://youtu.be/seVgmehFYdM


## Technology
Python and its various external and internal libraries:
- `requests` to make HTTP requests in Python
- `bs4` to scrape information from web pages
- `selenium` to automate web browser interaction (here, scrolling)
- `pandas` to manipulate data
- `advertools` to exclude some pre-existing sets of words 
- `matplotlib` to create visualizations
- `seaborn` to create visualizations 
- `wordcloud` to generate a word cloud (who would have thought)
- `numpy` to work with arrays

- `os` to use operating system dependent functionality
- `time` for time-related functions
- `collections` for a dict subclass for counting hashable objects
- `random` to implement pseudo-random numbers


## Limitations
- I needed to use selenium to access a browser and scroll through the page. I choose to go with Firebox and haven't written the code to support other browsers. Therefore, it requires Firefox to run this script. 
- After scrolling this 'very well-known site' first page of results, we obtain 175 job offers. Since that was enough for my purpose, I'm only using those 175 job offers.
- I sometime get 429 responses from the 'very well-known site' server. And therefore needed to add a timer between requests. I don't know what should be the minimum time between two requests and I also decided to go with something random for possible bot detection from the 'very well-known site'.


## License
This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/).