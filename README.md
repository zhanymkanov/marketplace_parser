## About
Project helps to parse https://kaspi.kz/shop/ (largest Kazakhstani marketplace) products and reviews using its API.

Products crawler (`spiders/list.py`) saves data by category in .json file with products information such as:
1. ID
2. Shop link
3. Price
4. Number of reviews
5. Category

Then, reviews crawler (`spiders/reviews.py`):
1. Walks through these json files
2. Makes a GET request to an API using product's ID and category for receiving .json list of its reviews
3. Crawler saves the data separating it by category folders, whereas each product has its own .json file with all downloaded reviews.

<i>
  Although, kaspi's API is not private, it is not public either. 
  
  I had to do some stuff with my outgoing traffic in order to find out its endpoints. 
  
  Therefore, I think it is not thetical to put it online, but to share it with anyone who might need it.
</i>

## Installation
```
git clone https://github.com/n1EzeR/kaspi_parser/
```
## Parser usage
```
pip install pipenv
pipenv install
pipenv shell
cd code
```
Run products_crawler.py to scrap information about all products among chosen (uncommented) categories

Run reviews_crawler.py to collect all reviews of each already scrapped products

## TODO
1. Actually parse the detailed information of each product
