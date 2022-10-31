# Scaping app and Docker

### What the project demonstrates
This project is about an app in Python, which drives a remote Selenium Chrome browser to render websites and then access the attributes of chosen elements. The project demonstrates a use of Selenium standalone browser, mapping a class and connecting to a database using SQLAlchemy and asynchronous rendering of a webpage while storing data in a database. There is also a Flask app, which is used as a more user friendly way to look up the desired output in the database.
The app is divided into four micro-services:
* The selenium standalone browser
* The database
* The scraping app
* The flask app
The microservices are containerized using Docker, where the selenium and database services are just based on the images from a Docker Hub, the flask app and the scraping app have their own dockerfile to be built according to the .py files and the dependencies.
In this repo, there are two docker.compose.yml files. One spins the containers necessary to add new data into the database, the second one spins the containers, which are necessary to view the data in a specific way, which is described below.

### What is it for
The app is built for one specific purpose - it tracks a price history of ads of a popular real estate website. Any new visitor has no recollection of what the prices were like, before they enterred the market. With this app, they can just enter the ad ID into the flask app's search bar and they will be served with a list of price changes on the ad. 
This is very useful information for price negotiations, since you can see independently, which seller actually is flexible on the price and who is not and also, how long and ad has been on. 

### NOTE
The areas in which the srape app searches for ads is defined in the ad_areas.txt file. If you want to search in different areas, you just need to add extra lines in this txt file, in the docker-compose file, there is a bind mount defined, that will mount this file with the internal directory of the scrape app's container.



