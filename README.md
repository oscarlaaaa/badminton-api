# BWF Match/Player API

## Overview
A simple API that has scraped match data from tournamentsoftware.com stored in an SQL database, and can return the match history of a player from between
2007 and present day as well as simple stats.

Note: This project is not affiliated with BWF or Tournamentsoftware in any way, shape, or form and does not profit from the data gathered.

## How to Use
1. Clone the repository onto a local machine
2. pip install all the required dependencies (outlined in requirements.txt inside of the bwfapi folder)
3. Run the bwf_scraper.py script from the root folder 
4. Wait for the script to finish running
5. Open the benchmarks/scraping.csv for benchmarks

## Tasks to Complete
- [x] Scrape matches from relevant event and return list of Matches
- [x] Compile list of BWF Tournaments either manually or through web-scraping
- [x] Make match data stored more complex to allow for greater data points (ex. time of day, bwf tournament level, etc.)
- [x] Concurrent scraping for tournament gatherer
- [x] Concurrent scraping for match gatherer
- [x] Concurrent scraping for player gatherer
- [x] Establish benchmarking to determine bottlenecks within scraping/data insertion process
- [x] Build foundation for MySQL-scraper interface to insert scraped data
- [ ] Load all scraped data onto hosted AWS MySQL server
- [x] Refactor and clean-up scraper code
- [ ] Establish back-end API foundation for db updates using Flask 
- [ ] Establish API endpoints to facilitate simple JSON transfer
- [ ] Refactor and clean-up API code
- [ ] Build simple static landing page to show people how to use the API

## Technologies Used
* Python3
* Flask
* MySQL 
* AWS (soon)