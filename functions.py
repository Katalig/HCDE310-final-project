import urllib.request
import json

DND_API_BASE_URL = 'https://www.dnd5eapi.co/api/'

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


# create_parsed_monster_data_dictionary(unparsed_data)
#
# Parameters
# 
# * Unparsed_data: A dictionary of unparsed data about a specific monster from
#                  the DND 5e API.
#
# Returns
#
# A new dictionary of specific usable information about a monster.
#
def create_parsed_monster_data_dictionary(unparsed_data):
    parsed_data = json.loads(unparsed_data)
    parsed_dict = {'name': parsed_data['name'],
                   'creature-type': parsed_data['type'],
                   'speeds': parsed_data['speed'],
                   'alignment': parsed_data['alignment'],
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

    monster_abilities = parsed_data['special_abilities']
    ability_lst = []
    for ability in monster_abilities:
        ability_lst.append(ability['name'])
    parsed_dict['abilities'] = ability_lst

    return parsed_dict


# monster_search(monster)
#
# Parameters

# * monster: The unformated name of a monster.
#
# Returns
#
# A translated dictionary of usable information about a monster to be
# adapted to the HTML.
#
def monster_search(monster):
    url = create_dnd_api_url(monster)
    data = get_api_data(url)
    results = {}
    if data is None:
        return results
    worked_data = create_parsed_monster_data_dictionary(data)
    print(worked_data)

    results['Name'] = worked_data['name']

    results['Creature Type'] = str(worked_data['creature-type']).capitalize()

    movement = worked_data['speeds']
    walk_speed = int(str(movement['walk']).split()[0])
    if walk_speed < 30:
        walk_pace_str = 'on the ground this creature cannot keep pace with a commoner'
    elif walk_speed > 30:
        walk_pace_str = 'on the ground this creature outpaces a commoner'
    else:
        walk_pace_str = 'on the ground this creature keeps pace with a commoner'
    del movement['walk']
    if len(movement) > 0:
        other_movement_str = 'This creature can '
        for speed in movement.keys():
            other_movement_str = other_movement_str + str(speed) + ', '
        results['Movement Speed'] = other_movement_str + 'and ' + walk_pace_str
    else:
        results['Movement Speed'] = walk_pace_str.capitalize()

    alignment = worked_data['alignment']
    if 'lawful' in alignment:
        if 'good' in alignment:
            results['Alignment'] = 'This creature is inclined towards Good and Order'
        if 'evil' in alignment:
            results['Alignment'] = 'This creature is inclined towards Evil and Order'
        else:
            results['Alignment'] = 'This creature is inclined towards Law and Order'
    elif 'chaotic' in alignment:
        if 'good' in alignment:
            results['Alignment'] = 'This creature is inclined towards Good and Impulsiveness'
        if 'evil' in alignment:
            results['Alignment'] = 'This creature is inclined towards Evil and Impulsiveness'
        else:
            results['Alignment'] = 'This creature is inclined towards Chaos and Impulsiveness'
    elif 'good' in alignment:
        results['Alignment'] = 'This creature is inclined towards Good and Selflessness'
    elif 'evil' in alignment:
        results['Alignment'] = 'This creature is inclined towards Evil and Selfishness'
    elif 'non-good' in alignment:
        results['Alignment'] = 'This creature acts against the forces of good'
    elif 'non-lawful' in alignment:
        results['Alignment'] = 'This creature acts against the forces of law'
    elif 'non-evil' in alignment:
        results['Alignment'] = 'This creature acts against the forces of evil'
    elif 'non-chaotic' in alignment:
        results['Alignment'] = 'This creature acts against the forces of chaos'
    elif 'unaligned' in alignment:
        results['Alignment'] = 'This creature does not function on the alignment spectrum'
    else:
        results['Alignment'] = 'This creature is neutrally inclined and does not embody any extremes'

    armor_class = worked_data['AC']
    if armor_class <= 10:
        results['Armor Class'] = 'This creature is very susceptible to direct attacks'
    elif armor_class <= 15:
        results['Armor Class'] = 'This creature is reasonably susceptible to direct attacks'
    elif armor_class <= 20:
        results['Armor Class'] = 'This creature is not very susceptible to direct attacks'
    elif armor_class <= 25:
        results['Armor Class'] = 'This creature is remarkably not susceptible to direct attacks'
    else:
        results['Armor Class'] = 'This creature is practically impenetrable'

    strength = worked_data['str']
    if strength <= 5:
        results['Strength'] = 'This creature has very low strength'
    elif strength <= 10:
        results['Strength'] = 'This creature has the strength of an average commoner'
    elif strength <= 15:
        results['Strength'] = 'This creature has decent strength'
    elif strength <= 20:
        results['Strength'] = 'This creature has great strength'
    elif strength <= 25:
        results['Strength'] = 'This creature has remarkable inhuman strength!'
    else:
        results['Strength'] = 'This creature has unmatched incredible strength!!!'

    dexterity = worked_data['dex']
    if dexterity <= 5:
        results['Dexterity'] = 'This creature has very low dexterity'
    elif dexterity <= 10:
        results['Dexterity'] = 'This creature has the dexterity of an average commoner'
    elif dexterity <= 15:
        results['Dexterity'] = 'This creature has decent dexterity'
    elif dexterity <= 20:
        results['Dexterity'] = 'This creature has great dexterity'
    elif dexterity <= 25:
        results['Dexterity'] = 'This creature has remarkable inhuman dexterity!'
    else:
        results['Dexterity'] = 'This creature has unmatched incredible dexterity!!!'

    constitution = worked_data['con']
    if constitution <= 5:
        results['Constitution'] = 'This creature has very low constitution'
    elif constitution <= 10:
        results['Constitution'] = 'This creature has the constitution of an average commoner'
    elif constitution <= 15:
        results['Constitution'] = 'This creature has decent constitution'
    elif constitution <= 20:
        results['Constitution'] = 'This creature has great constitution'
    elif constitution <= 25:
        results['Constitution'] = 'This creature has remarkable inhuman constitution!'
    else:
        results['Constitution'] = 'This creature has unmatched incredible constitution!!!'

    intelligence = worked_data['int']
    if intelligence <= 5:
        results['Intelligence'] = 'This creature has very low intelligence'
    elif intelligence <= 10:
        results['Intelligence'] = 'This creature has the intelligence of an average commoner'
    elif intelligence <= 15:
        results['Intelligence'] = 'This creature has decent intelligence'
    elif intelligence <= 20:
        results['Intelligence'] = 'This creature has great intelligence'
    elif intelligence <= 25:
        results['Intelligence'] = 'This creature has remarkable inhuman intelligence!'
    else:
        results['Intelligence'] = 'This creature has unmatched incredible intelligence!!!'

    wisdom = worked_data['wis']
    if wisdom <= 5:
        results['Wisdom'] = 'This creature has very low wisdom'
    elif wisdom <= 10:
        results['Wisdom'] = 'This creature has the wisdom of an average commoner'
    elif wisdom <= 15:
        results['Wisdom'] = 'This creature has decent wisdom'
    elif wisdom <= 20:
        results['Wisdom'] = 'This creature has great wisdom'
    elif wisdom <= 25:
        results['Wisdom'] = 'This creature has remarkable inhuman wisdom!'
    else:
        results['Wisdom'] = 'This creature has unmatched incredible wisdom!!!'

    charisma = worked_data['cha']
    if charisma <= 5:
        results['Charisma'] = 'This creature has very low charisma'
    elif charisma <= 10:
        results['Charisma'] = 'This creature has the charisma of an average commoner'
    elif charisma <= 15:
        results['Charisma'] = 'This creature has decent charisma'
    elif charisma <= 20:
        results['Charisma'] = 'This creature has great charisma'
    elif charisma <= 25:
        results['Charisma'] = 'This creature has remarkable inhuman charisma!'
    else:
        results['Charisma'] = 'This creature has unmatched incredible charisma!!!'

    vulnerabilities = worked_data['vulnerable']
    if len(vulnerabilities) != 0:
        if len(vulnerabilities) == 1:
            results['Damage Vulnerabilities'] = str(vulnerabilities[0]).capitalize()
        else:
            vulnerable_str = ''
            final_word = vulnerabilities[-1]
            final_word_str = 'and ' + str(final_word).capitalize()
            vulnerabilities.remove(final_word)
            for vulnerability in vulnerabilities:
                vulnerable_str = vulnerable_str + str(vulnerability).capitalize() + ', '
            results['Damage Vulnerabilities'] = vulnerable_str + final_word_str
    else:
        results['Damage Vulnerabilities'] = 'None'

    resistances = worked_data['resistant']
    if len(resistances) != 0:
        if len(resistances) == 1:
            results['Damage Resistances'] = str(resistances[0]).capitalize()
        else:
            resist_str = ''
            final_word = resistances[-1]
            final_word_str = 'and ' + str(final_word).capitalize()
            resistances.remove(final_word)
            for resistance in resistances:
                resist_str = resist_str + str(resistance).capitalize() + ', '
            results['Damage Resistances'] = resist_str + final_word_str
    else:
        results['Damage Resistances'] = 'None'

    damage_immunities = worked_data['dmg-immune']
    if len(damage_immunities) != 0:
        if len(damage_immunities) == 1:
            results['Damage Immunities'] = str(damage_immunities[0]).capitalize()
        else:
            dmg_immune_str = ''
            final_word = damage_immunities[-1]
            final_word_str = 'and ' + str(final_word).capitalize()
            damage_immunities.remove(final_word)
            for immunity in damage_immunities:
                dmg_immune_str = dmg_immune_str + str(immunity).capitalize() + ', '
            results['Damage Immunities'] = dmg_immune_str + final_word_str
    else:
        results['Damage Immunities'] = 'None'

    condition_immunities = worked_data['condition-immune']
    if len(condition_immunities) != 0:
        if len(condition_immunities) == 1:
            results['Condition Immunities'] = str(condition_immunities[0]).capitalize()
        else:
            con_immune_str = ''
            final_word = condition_immunities[-1]
            final_word_str = 'and ' + str(final_word).capitalize()
            condition_immunities.remove(final_word)
            for immunity in condition_immunities:
                con_immune_str = con_immune_str + str(immunity).capitalize() + ', '
            results['Condition Immunities'] = con_immune_str + final_word_str
    else:
        results['Condition Immunities'] = 'None'

    abilities = worked_data['abilities']
    if len(abilities) > 0:
        if len(abilities) == 1:
            results['Abilities'] = 'This creature has the following ability: ' + abilities[0]
        else:
            abilities_str = 'This creature also has the following abilities: '
            final_ability = abilities[-1]
            final_ability_str = 'and ' + str(final_ability)
            abilities.remove(final_ability)
            for ability in abilities:
                abilities_str = abilities_str + ability + ', '
            results['Abilities'] = abilities_str + final_ability_str
    print(results)
    return results



def main():
    pass


if __name__ == "__main__":
    try:
        main()
    except (NameError, SyntaxError):
        pass
