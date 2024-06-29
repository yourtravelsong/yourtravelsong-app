import json
import wikipediaapi
from config import settings
import os

wiki_wiki = wikipediaapi.Wikipedia(
    f'WorldCities ({settings.EMAIL})',
    'en'
)

def get_city_info(city_name, path = '../data/cities'):
    cityPath = f'{path}/{city_name}.txt'
    if os.path.exists(cityPath):
        print("Already analyzed ", city_name)
        return None

    os.makedirs(path, exist_ok=True)
    page = wiki_wiki.page(city_name)
    if page.exists():
        with open(cityPath, 'w') as f:
            f.write(page.text)
            return page.text
    else:
        return None
    
if __name__ == '__main__':
    world_cities = json.load(open('world_cities_top500.json'))['world_cities']
    for city in world_cities:
        get_city_info(city)
