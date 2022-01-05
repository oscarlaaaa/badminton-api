# BWF Match/Player API

## Overview
A simple API that has scraped match data from tournamentsoftware.com stored in an SQL database, and can return the match, tournament, and opponent history of a player from between 2007 and present day. The database is automatically updated periodically every week.

Note: This project is not affiliated with BWF or TournamentSoftware in any way, shape, or form and does not profit from the data gathered.

## How to Use
1. Clone the repository onto a local machine
2. pip install all the required dependencies (outlined in requirements.txt inside of the bwfapi folder)
3. Open a terminal and navigate into the /bwfapi folder
4. Run the following command:  ```uvicorn server:app --reload```
5. Open a web browser and navigate to ```localhost:8000```

## Tasks to Complete
- [x] Scrape matches from relevant event and return list of Matches
- [x] Compile list of BWF Tournaments either manually or through web-scraping
- [x] Make match data stored more complex to allow for greater data points (ex. time of day, bwf tournament level, etc.)
- [x] Concurrent scraping for tournament gatherer
- [x] Concurrent scraping for match gatherer
- [x] Concurrent scraping for player gatherer
- [x] Establish benchmarking to determine bottlenecks within scraping/data insertion process insertion process
- [x] Build foundation for MySQL-scraper interface to insert scraped data
- [X] Refactor and clean-up scraper code
- [x] Establish back-end API foundation for periodic DB updates using FastAPI
- [X] Set-up SQLAlchemy models and DB connection
- [X] Establish API endpoints to facilitate simple JSON get requests
- [X] Refactor and clean-up API code
- [X] Build simple static landing page to show people how to use the API
- [ ] Build Docker Image
- [ ] Load all scraped data onto hosted AWS MySQL server
- [ ] Deploy onto cloud-service like AWS or Heroku

## Technologies Used
* Python3 (BeautifulSoup, Aiohttp)
* FastAPI (SQLAlchemy)
* MySQL 
* AWS or Heroku (soon)