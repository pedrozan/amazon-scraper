import csv
import os
from datetime import datetime

import click
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def get_firefox_driver():
    url = "https://www.amazon.com.br/"
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(30)
    driver.get(url)

    return driver


def write_to_csv(kindle_price, hard_cover_price):
    # The path variable will point to the output file
    path = "./prices.csv"

    # The structure of the CSV file is given here
    header = ["date", "kindle", "hard cover"]
    row = [datetime.now(), kindle_price, hard_cover_price]

    # We test if the file already exists if it does, we just append
    # else we create it.
    if os.path.isfile(path) and os.access(path, os.R_OK):
        with open(path, "a") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(row)
    else:
        with open(path, "wt") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(header)
            csv_writer.writerow(row)


@click.command(
    help="""
    Receives a product name and searches for it on Amazon, if the product is found,
    will save the price for the Kindle and hard cover versions.
    """
)
@click.argument("product")
def fetch_prices(product):
    # Get the driver and website on Firefox headless
    driver = get_firefox_driver()

    # Search for the product on search box
    search_field = driver.find_element_by_id("twotabsearchtextbox")
    search_field.click()
    search_field.send_keys(product)
    search_field.send_keys(Keys.ENTER)

    # Access product's page
    product_link = driver.find_element_by_partial_link_text(product)
    product_link.click()

    # Read raw prices for Kindle and hard cover versions
    raw_kindle_price = driver.find_element_by_css_selector(
        "#a-autoid-8-announce > span:nth-child(3) > span:nth-child(1)"
    )
    raw_hard_cover_price = driver.find_element_by_css_selector(
        "#a-autoid-9-announce > span:nth-child(3) > span:nth-child(1)"
    )

    # Format prices to be saved as integers
    formated_kindle_price = float(raw_kindle_price.text[2:].replace(",", "."))
    formated_hard_cover_price = float(raw_hard_cover_price.text[2:].replace(",", "."))

    # Close the driver as we don't need it anymore
    driver.close()

    # Write data to CSV file
    write_to_csv(formated_kindle_price, formated_hard_cover_price)


if __name__ == "__main__":
    fetch_prices()
