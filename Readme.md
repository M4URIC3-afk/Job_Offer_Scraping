# Finding the most in-demand programming languages from Linkedin Job Offers
-----------
This Python notebook scrapes the most recent Linkedin Job Offers for a given job title and tells what are the most in-demand programming languages based on their occurences. 

It is currently set up for job offers written in French or English.
Also, it is currently set up to use Mozilla Firefox as a browser (in order to scroll through the page).

See 'Main.ipynb' for detailed presentation.


## Description
I'm currently retraining to become a Data specialist. Since I will soon be looking for a job, I thought I should define what are the most in-demand programming languages and dashboarding tools. And could use python to do that.


## Technology
Python and its various libraries:
- `requests` to make HTTP requests in Python
- `bs4` to scrape information from web pages
- `selenium` to automate web browser interaction (here, scrolling)
- `pandas` to manipulate data
- `advertools` to exclude some pre-existing sets of words 
- `matplotlib.pyplot` to create visualizations
- `wordcloud` to generate a word cloud (who would have thought)
-  `numpy` to work with arrays etc.

- `os` to use operating system dependent functionality
- `re` for regular expression matching operations
- `time` for time-related functions
- `collections` for a dict subclass for counting hashable objects
- `random` to implement pseudo-random number generators


## Limitations

- I needed to use selenium to access a browser and scroll through the page. Since I used it, I choose to go with Firebox. I haven't written the code to support other browsers. In short, it requires Firefox in order to run this script. 
- After scrolling, Linkedin first page of results include around 150 offers. Since that was enough for my purpose, I'm only using those.
- The Scraping job offers code snippet is a bit ugly for different reasons. Some requests were returning 429 and I needed to add a timer. I don't know what should be the minimum time between two requests and I also decided to go with something random for possible bot detection from Linkedin. After some testing, I decided to just print out http 429 errors and not try again on these get requests. Lastly, I'm also using job_info_str variable to store some added content that I ended-up not using but could be usefull to extract job titles, employers, type of contract etc. For all these reasons, this code snipet isn't ideal but it does the job for now. 


## Licence
This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/). 