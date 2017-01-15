Python microservice API
=============================

Example project to implement a Python messaging API microservice.


Getting Started
-------------------------
This project requires internet connection, docker and docker-compose on the host machine.




Deployment
-------------------------

Build the image
	docker-compose build
	
Launch it
	docker-compose up




Documentation
-------------------------

There are two end points:

/ADD
Add a data point

curl "http://localhost/add?account_no=123&date=2017-01-01&ledger_balance=10&cleared_balance=10"

this will return a JSON with a single field ID_CODE like the following:

{
  "ID_CODE": "0"
}

/VISUALIZE
Visualize the data

curl http://localhost/visualize?account_no=123

vill return an http page with a chart with the data, rolling average and exponential average.




Testing
-------------------------------
Run the tests with 

python test_units.py








Technology Stack / Dependencies
-------------------------------
- Python 3.5  - All components are build in Python
- Nginx       - HTTP Proxy to sitting in front of the Python Service
- Flask       - Web application framework suitable for creating microservices in Python.
- Gunicorn    - Pre-fork application server to efficiently serve the Flask application in production.
- Docker      - Container technology to create simple and consistent deployments.

