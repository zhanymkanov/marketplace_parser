# About
The project helps to crawl the largest Kazakhstani marketplace.

## Parsed data can be downloaded here:
https://github.com/zhanymkanov/reviews_dataset
- Partially cleaned (both raw and cleaned versions are available though)
- ~190k rows

# How it works
## Parser steps
1. Crawl products JSON lists
2. Crawl reviews based on products list
3. Crawl laptops, PCs, smartphones specs based on products list
4. Cleans the collected JSON files and extracts valuable information from the specifications
5. Dumps data into the database

### Comment on API access
<i>
  Although API is not private, it is nor public.

  I had to do some stuff with my outgoing traffic to find out its endpoints. 

  Therefore, I think it is not tethical to put it online, but to say that is easy to get them
</i>

## Installation
### Prerequisites
1. Python 3.6+
2. Docker, docker-compose

### Installation steps
1. Download the project
```
git clone https://github.com/zhanymkanov/reviews_parser
```
2. Set up the container
```
docker-compose build
```

## Parser usage
To run the app you need to know API endpoints, which is currently not available to be shared, but discovered by yourselves.
If you have them, modify the main.py so that you parse only required categories.
For the first time, I recommend you to run the `main.py` 3 times:
1. First, run for products
2. Second and third times for either reviews or product specifications

