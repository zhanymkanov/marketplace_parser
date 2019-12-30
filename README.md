# About
The project helps to parse the largest Kazakhstani marketplace: products and reviews using its API.

## Parsed data can be downloaded here:
https://github.com/n1EzeR/russian_reviews_dataset
- Partially cleaned (both row and cleaned versions are available though)
- ~120k rows

# Parser
## Parser steps
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
  Although API is not private, it is nor public. 
  
  I had to do some stuff with my outgoing traffic to find out its endpoints. 
  
  Therefore, I think it is not tethical to put it online.
</i>

## Installation
### Prerequisites
1. Python 3.6+
2. pip
3. pipenv (`pip install pipenv`)

### Installation steps
1. Download the project
```
git clone https://github.com/n1EzeR/reviews_parser
```
2. Go to project directory
```
cd reviews_parser
```
3. Install the packages and virtual environment
```
pipenv install
```

## Parser usage
```
pipenv shell
cd code
```
Run the products crawler to scrap information about all products among chosen (uncommented) categories in `products_crawler.py`.

```
python products_crawler.py
```


Run reviews crawler to collect all reviews of each already scrapped products. 

```
python reviews_crawler.py
```

Although, it is possible to run them all at once, I recommend you to parse reviews one by one (comment/uncomment categories), so that you could check each category integrity

## Further development
1. Parse the detailed information of each product
