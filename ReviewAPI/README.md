Review API
Flipkart and Amazon
Dependencies are specified in requirements.txt

For linux machines, Chromedriver should be installed with package manager(Eg, For Ubuntu)
sudo apt install chromium-chromedriver

install all these requirements in python virtualenv using:
pip install -r requrirements.txt

Run API using:
python app.py

API usage:

For REST Services:
http://localhost:5000/flipkart?url=<Flipkart product review URL>

http://localhost:5000/amazont?url=<Amazon product review URL>

http://localhost:5000?q=<queryString>&no_of_products=<numberof products>&no_of_reviews_per_products=<number of reviews per product>

To run as a normal program, run, (only query string is supported)
python query.py
Fetched results are stored in a csv file named result.csv

This is the initial Code done for data collection. 
Code used for frontend are inside frontend folder