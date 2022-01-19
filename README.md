# BWF Badminton API
![Landing page](https://i.imgur.com/sbkgNVp.png)

A badminton singles match API that has scraped match data from tournamentsoftware.com stored in an SQL database from between 2007 and present day. The database is automatically updated periodically every month. Endpoints for players, matches, and tournaments are all established in the application. 

Right now the database only supports Singles events (Men's and Women's), but the API may expand to accommodate Doubles events in the future.

## Current Features
* Regular database updates scraped directly from TournamentSoftware every month
* Multiple endpoints to facilitate various datapoint collections
* Flexible endpoint queries to provide limits, parameters, and more
* Landing page with detailed API usage instructions + FastAPI generated /docs page
* Async-focused design for robust responsiveness
* A very cool creator :sunglasses:

## Motivation
This project is made for the purpose of providing data for a data analysis/visualization project which is in the works. Stay tuned!

## How to Use
Visit [here](https://badminton-api.com/ "Badminton API") for detailed information on how to access the various endpoints of the API.

Visit [here instead](https://badminton-api.com/docs "Badminton API FastAPI Docs") for the FastAPI-generated documentation, or to test out the various endpoints.

## Progress Roadmap
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
- [x] Build Docker Image
- [x] Load all scraped data onto hosted AWS MySQL server
- [X] Deploy onto cloud-service like AWS or Heroku

## Technologies Used
* Python3 (BeautifulSoup, Aiohttp, SQLAlchemy)
* FastAPI 
* MySQL (AWS RDS)
* AWS Lambda/Amplify/Gateway

## How Can I Contribute?
If you'd like more or different endpoints for the project, feel free to clone the project, establish local database credentials in a .env file in the root folder, and submit a pull request. You can also test out the various endpoints and let me know if there are any bugs or convenience issues!

### Credits
Special thanks to [Vivian](http://github.com/vvnwu) for helping me debug stuff