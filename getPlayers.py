import pandas as pd
import json
import csv
import sys
import os


player_csv = r'C:\Users\rasmu\WebstormProjects\backend\python\players_21.csv'

def load_attributes():
    """
    :return:
        attribute_list: all attributes for Players to search
        positionen:     all positions of Players
    """
    with open(player_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        row1 = next(reader)
    indices = [3, 5, 8, 12, 20, 21] + list(range(24, 60)) + list(range(72, 78))
    attribute_list = [row1[i] for i in indices]
    positionen = [row1[i] for i in range(79, 106)]
    # return json
    return attribute_list, positionen


def load_data(col=True):
    if col:
        return pd.read_csv(player_csv, low_memory=False, encoding="utf-8")
    else:
        return pd.read_csv(player_csv, low_memory=False, usecols=["Name"], encoding="utf-8")


def search_player(name="", position="-", age=99, attribute1="-", value1=99, attribute2="-", value2=99):
    """
    filters df for all params that aint empty
    :return:
    """
    df = load_data()
    if name != "":
        df = df[df.Name == name]
    if position != "-":
        df = df[df.BP == position]
    if age != 99:
        df = df[df.Age >= age]
    if attribute1 != "-":
        df = df[df[attribute1] >= int(value1)]
    if attribute2 != "-":
        df = df[df[attribute2] >= int(value2)]
    return df


def handle_request(json_data):
    """

    :param json_data: json request from search
    :return:
        json that has all infos about filtered players
    """
    req = json.loads(json_data)
    players = search_player(req['name'], req['position'], req['age'], req['ability1Name'], req['ability1Value'],
                            req['ability2Name'], req['ability2Value'])
    return players.to_json(orient="split")


def get_suggestion(subname):
    series = load_data(False)
    name_suggest = [name for name in series['Name'].to_list() if subname in name]
    return name_suggest

'''
if __name__ == "__main__":
    req_json = '{ "name":"" , "position":"-" , "age":30, "ability1Name":"POT", "ability1Value":80 ,' \
               '"ability2Name":"OVA", "ability2Value":80}'

    print(get_suggestion("Ronal"))
    (attributes, positions) = load_attributes()
    json = handle_request(req_json)
    print(json)
'''    
   
data = None

if sys.argv[1] == "attributes":
    data = load_attributes()
    

if sys.argv[1] == "getPlayers":
    data = handle_request(sys.argv[2])
    
    
if sys.argv[1] == "suggest":
    data = get_suggestion(sys.argv[2])
    # data= data.encode('utf-8')
    
print(data)


