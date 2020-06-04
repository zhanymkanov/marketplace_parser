# About
The project helps to crawl the largest Kazakhstani marketplace.

## Parsed data can be downloaded here:
https://github.com/zhanymkanov/reviews_dataset
- Partially cleaned (both raw and cleaned versions are available though)
- ~190k rows

# How it works
## Parser steps
1. Use Products API to get JSON List of the products
2. Use Products JSON List to crawl Products Specifications from HTML pages
3. Use Products JSON List to request Reviews API for every product
4. Clean the collected JSON files and extract valuable information from the specifications
5. Dump data into the database

### Comment on API access
<i>
  Although API is not private, it is nor public.

  I had to do some stuff with my outgoing traffic to find out its endpoints. 

  Therefore, I think it is not tethical to put it online.
</i>

## Installation
### Prerequisites
1. Python 3.6+
2. Docker - optional

### Installation steps
1. Get the project
```
git clone https://github.com/zhanymkanov/reviews_parser
```
2a. Install the packages without docker
```
pip install -r requirements/base.txt
```
2b. Install the packages with docker
```
docker-compose up -d --build
```
