# BWF Web Scraper API

## Overview
A simple web scraper API that scrapes tournament data, compiles the data, and feeds the dataset into a ML model to generate predictive analytics about tournament results (that's the plan, at least).

## How to Use
1. Clone the repository onto a local machine
2. pip install all the required dependencies (outlined in requirements.txt inside of the bwfapi folder)
3. Run the main_scraper.py script (change the year on line 15 to your desired year) 
4. Wait for it to finish (usually takes ~90 seconds per year)
5. Open the scraped_data.csv for your information! (soon to implement into MySQL DB)

## Features to Implement
- [x] Scrape matches from relevant event and return list of Matches
- [x] Compile list of BWF Tournaments either manually or through web-scraping
- [x] Make match data stored more complex to allow for greater data points (ex. time of day, bwf tournament level, etc.)
- [x] Concurrent scraping for tournament gatherer
- [x] Concurrent scraping for match gatherer
- [x] Establish benchmarking to determine best async implementation (or if it's even needed)
- [ ] Either compile/analyze data before storing into MongoDB OR store all data and compile from db when necessary
- [ ] Make scraper compatible with doubles events?
- [ ] Establish back-end API using Flask
- [ ] Establish front-end webpage; maybe React
- [ ] Attempt to implement various ML algorithms - maybe start with Linear Regression? time to study more
- [ ] Build predictive-analytics system by utilizing dataset + various ML models to calculate H2H % of victory
- [ ] Figure out how to use the above to establish tournament most likely winners

## Technologies Used
* Python3 and Django/Flask (soon)
* React.js (soon)
* MongoDB