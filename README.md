# BWF Match-set API

## Overview
A simple API that has scraped match data from tournamentsoftware.com stored in an SQL database, and can return the match history of a player from between
2007 and present day as well as simple stats.

## How to Use
1. Clone the repository onto a local machine
2. pip install all the required dependencies (outlined in requirements.txt inside of the bwfapi folder)
3. Run the main_scraper.py script from the root folder 
4. Wait for it to finish (usually takes ~300 seconds per year)
5. Open the benchmarks/scraping.csv for benchmarks or web_scraper/db for all data scraped

## Features to Implement
- [x] Scrape matches from relevant event and return list of Matches
- [x] Compile list of BWF Tournaments either manually or through web-scraping
- [x] Make match data stored more complex to allow for greater data points (ex. time of day, bwf tournament level, etc.)
- [x] Concurrent scraping for tournament gatherer
- [x] Concurrent scraping for match gatherer
- [x] Establish benchmarking to determine best async implementation (or if it's even needed)
- [ ] Load all scraped data onto hosted AWS MySQL server
- [ ] Establish back-end API foundation using Flask 

## Technologies Used
* Python3
* Flask
* MySQL 