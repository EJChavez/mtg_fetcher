import csv
from pandas import DataFrame
import requests
import json


def main():
    with open('card_names.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = ['Name', 'Card Type', 'CMC', 'Identity', 'Price']
        data = DataFrame([header])
        for name in csv_reader:
            print(name)
            card_list = get_api(name)
            data = data.append([card_list], ignore_index=True)
            data.to_csv('card_data.csv', index=False)


def get_api(cardname):
    res = requests.get(f'https://api.scryfall.com/cards/named?fuzzy={cardname}')
    # print(res.status_code)
    api_dict = json.loads(res.text)
    important_list = clean_dictionary(api_dict)
    return important_list


def clean_dictionary(temp_dict):
    # print(temp_dict)
    name = temp_dict['name']
    # picture = temp_dict['image_uris']['normal']
    price_usd = temp_dict['prices']['usd']
    price_foil = temp_dict['prices']['usd_foil']
    price = clean_price(price_usd, price_foil)
    raw_identity = temp_dict['color_identity']
    color_identity = clean_color_identity(str(raw_identity))
    cmc = temp_dict['cmc']
    card_type = temp_dict['type_line']
    cleaned_list = [name, card_type, cmc, color_identity, price]
    return cleaned_list


def clean_price(usd, foil):
    if usd:
        return float(usd)
    if not usd:
        if foil:
            return float(foil)
        else:
            return None


def clean_color_identity(string):
    string = string.replace("'",'')
    if string == '[]':
        return '[C]'
    else:
        return string

if __name__ == '__main__':
    main()

