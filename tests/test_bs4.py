from parsers.parser_bs4 import parse_recipe
import json


def test_status():

    result_post, response = parse_recipe('https://www.iamcook.ru/event/everyday/everyday-vegetarian',
                                            pages=1, dish_type="Вегетарианская")
    assert response == 200
    print("status code is 200")


def check_json():
    print("Проверка ключей")
    with open('recipes_bs4.json', 'r') as file:
        recipes = json.loads(file)

    keys = ['dishtype', 'title', 'description', 'ingredients', 'imgs_url', 'calories']

    check_keys = recipes[0].keys()
    assert check_keys == keys


def check_recipes():
    print("Проверка наполненности json файла")
    with open('recipes_bs4.json', 'r') as file:
        recipes = json.loads(file)

    for recipe in recipes:
        if not recipe.values():
            check = 'Bad'
        else:
            check = 'Good'

    assert check == 'Good'
