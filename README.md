# amazon-scraper
This is a simple scraper that goes to Amazon.com and searches for a product to read its price.

## Installing
You will need to first [install Python 3](https://www.python.org/downloads/) and [set up Firefox's driver](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/).

If you already have Python 3 and Firefox driver on your system just clone this repo, `cd` into the project's folder and do a `pip install`
```
$ git clone https://github.com/pedrozan/amazon-scraper
$ cd amazon-scraper
$ pip install -r requirements.txt
```

## Running
After installing all the dependencies run with `python scraper.py "product name"`. It will start a headless Firefox instance, navigate to amazon.com and search for "produc name".
If the product is found the prices will be saved to prices.csv on the same folder.
