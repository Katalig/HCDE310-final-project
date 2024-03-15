import urllib.request
import json

DND_API_BASE_URL = 'https://www.dnd5eapi.co/api/'

#
# create_monster_api_url(place)
#
# Parameters:
#
# * monster: A string that denotes the name of a monster
#            for which the api url for that monster should be returned.
#
# Returns:
#
# string that contains the url for a specific monster in the dnd api.
# 
#
def create_dnd_api_url(imput):
    lower_imput = imput.lower()
    final_imput = lower_imput.replace(' ', '-')
    return(str(DND_API_BASE_URL) + 'monsters/' + str(final_imput))


def get_api_data(url):
    try:
        requested_url = urllib.request.urlopen(url)
        data = requested_url.read()
        return data
    except IOError:
        return None

#
# wikipedia_locationsearch(place, max_results=10, radius=2.0, sort=False)
#
# Parameters
# 
# * place: A string that denotes the name of a place, or an address (e.g., 
#          "University of Washington" or "1410 NE Campus Parkway, Seattle, WA 
#          98195") around which the search results should be returned.
# * max_results: An integer that denotes the maximum number of results that 
#                should be returned by the function. 
#                Default value: 10.
# * radius: A float that denotes the number of miles within which the search
#           results should be restricted.
#           Default value: 2.0
# * sort: A boolean value indicating whether the results should be sorted by
#         the length of the articles or not.
#         Default value: False.
#
# Returns
#
# A list of wikipedia.WikipediaPage objects that match the search parameters.
# If no results are found, a blank list (`[]`) is returned.
#
#
def create_parsed_monster_data_dictionary(unparsed_data):
    parsed_data = json.loads(unparsed_data)
    # print(parsed_data)
    parsed_dict = {'name': parsed_data['name'],
                   'creature-type': parsed_data['type'],
                   'alignment': parsed_data['alignment'],
                   'cr': parsed_data['challenge_rating'],
                   'languages': parsed_data['languages'],
                   'hp': parsed_data['hit_points'],
                   'AC': parsed_data['armor_class'][0]['value'],
                   'str': parsed_data['strength'],
                   'dex': parsed_data['dexterity'],
                   'con': parsed_data['constitution'],
                   'int': parsed_data['intelligence'],
                   'wis': parsed_data['wisdom'],
                   'cha': parsed_data['charisma'],
                   'vulnerable': parsed_data['damage_vulnerabilities'],
                   'resistant': parsed_data['damage_resistances'],
                   'dmg-immune': parsed_data['damage_immunities']}

    monster_condition_immunities = parsed_data['condition_immunities']
    condition_immunity_lst = []
    for condition in monster_condition_immunities:
        condition_immunity_lst.append(condition['name'])
    parsed_dict['condition-immune'] = condition_immunity_lst

    monster_profs = parsed_data['proficiencies']
    for prof in monster_profs:
        parsed_dict[prof['proficiency']['name']] = prof['value']

    monster_speeds = parsed_data['speed']
    for speed in monster_speeds:
        parsed_dict[speed] = monster_speeds[speed]

    monster_senses = parsed_data['senses']
    for sense in monster_senses:
        parsed_dict[sense] = monster_senses[sense]

    monster_abilities = parsed_data['special_abilities']
    ability_lst = []
    for ability in monster_abilities:
        ability_lst.append(ability['name'])
    parsed_dict['abilities'] = ability_lst

    return parsed_dict

def monster_search(monster):
    url = create_dnd_api_url(monster)
    data = get_api_data(url)
    results = []
    if data is None:
        return results
    parsed_data = create_parsed_monster_data_dictionary(data)
    return parsed_data



## Code to test your function follows follows
def main():
    '''url = create_dnd_api_url('animated armor')
    data = get_api_data(url)
    parsed_data = create_parsed_monster_data_dictionary(data)
    print(parsed_data)'''
    print(monster_search('adult black dragon'))


if __name__ == "__main__":
    try:
        main()
    except (NameError, SyntaxError):
        pass 
