import json
import wikipediaapi
from config import settings
import os

wiki_wiki = wikipediaapi.Wikipedia(
    f'WorldCities ({settings.EMAIL})',
    'en'
)

def get_city_info(city_name):
    page = wiki_wiki.page(city_name)
    os.makedirs('../data/cities', exist_ok=True)
    if page.exists():
        
        with open(f'../data/cities/{city_name}.txt', 'w') as f:
            f.write(page.text)
    else:
        return None
    
if __name__ == '__main__':
    world_cities = json.load(open('world_cities.json'))['world_cities']
    for city in world_cities:
        get_city_info(city)
