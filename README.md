## About
The project helps to parse https://kaspi.kz/shop/ (largest Kazakhstani marketplace) products and reviews using its API.

Products crawler (`spiders/list.py`) saves data by category in JSON files with products information such as:
1. ID
2. Shop link
3. Price
4. Number of reviews
5. Category

Then, reviews crawler (`spiders/reviews.py`):
1. Walks through these JSON files
2. Makes a GET request to an API using product's ID and category for receiving .json list of its reviews
3. Crawler saves the data separating it by category folders, whereas each product has its JSON file with all downloaded reviews.

#### Comment on API access
<i>
  Although Kaspi's API is not private, it is nor public. 
  
  I had to do some stuff with my outgoing traffic to find out its endpoints. 
  
  Therefore, I think it is not tethical to put it online but I am willing to share it with anyone who might need it.
</i>

## Installation
```
git clone https://github.com/n1EzeR/kaspi_parser/
```
If you do not have pipenv installed, install it:

`pip3 install pipenv`

## Parser usage
```
pipenv install
pipenv shell
cd code
```
Run `python products_crawler.py` to scrap information about all products among chosen (uncommented) categories

Run `python reviews_crawler.py` to collect all reviews of each already scrapped products

## TODO
1. Parse the detailed information of each product
