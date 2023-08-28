import json
import time
from urllib.parse import urljoin

from pathvalidate import sanitize_filename
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def parse_recipes(url, pages, driver, dish_type):
    recipes_list = []
    for page in range(1, pages+1):
        recipes_url = f"{url}/{page}"
        driver.get(recipes_url)
        time.sleep(5)
        titles_elem = driver.find_elements(By.CLASS_NAME, 'header')
        titles = [title.text for title in titles_elem]
        descriptions_elem = driver.find_elements(By.CLASS_NAME, 'description')
        descriptions = [sanitize_filename(description.text) for description in descriptions_elem]
        ingredients_elem = driver.find_elements(By.CLASS_NAME, 'ingredients')
        ingredients = [(ingredient.text).replace("\n", " ") for ingredient in ingredients_elem]
        imgs_url_elem = driver.find_elements(By.CLASS_NAME, 'preimage')
        src_images = [img.get_attribute('src') for img in imgs_url_elem]
        base_url = "http://img.iamcook.ru/"
        imgs_url = [urljoin(base_url, img) for img in src_images]
        calories_elem = driver.find_elements(By.CLASS_NAME, 'energy')
        calories = [amount.text for amount in calories_elem]
        for element in range(len(titles)-1):
            recipes = {
                        "dishtype": "",
                        "title": "",
                        "description": "",
                        "ingredients": "",
                        "imgs_url": "",
                        "calories": "",
            }
            recipes["dishtype"] = dish_type
            recipes["title"] = titles[element]
            recipes["description"] = descriptions[element]
            recipes["ingredients"] = ingredients[element]
            recipes["imgs_url"] = imgs_url[element]
            recipes["calories"] = calories[element]
            recipes_list.append(recipes)
    return recipes_list


def main():
    driver_location = '/usr/bin/chromedriver'
    binary_location = '/usr/bin/google-chrome'
    vegetaian_url = "https://www.iamcook.ru/event/everyday/everyday-vegetarian"
    nonglyuten_url = 'https://www.iamcook.ru/event/baking/gluten-free-baking'
    meat_url = "https://www.iamcook.ru/showsubsection/myasnie_bluda"
    pages = 4
    options = webdriver.ChromeOptions()
    options.binary_location = binary_location
    service = Service(executable_path=driver_location)
    driver = webdriver.Chrome(service=service, options=options)
    time.sleep(5) 
    veg_recipes = parse_recipes(vegetaian_url, pages, driver,
                                dish_type="Вегетарианская")
    nonglyuten_list = parse_recipes(nonglyuten_url, pages, driver,
                                    dish_type="Безглютеновая")

    meat_list = parse_recipes(meat_url, pages, driver,
                              dish_type="Мясные блюда")
    recipes_list = veg_recipes + nonglyuten_list + meat_list

    with open('recipes_selenium.json', 'w') as fp:
        json.dump(
            recipes_list,
            fp,
            ensure_ascii=False,
            indent=4
        )

    driver.quit()


if __name__ == "__main__":
    main()
