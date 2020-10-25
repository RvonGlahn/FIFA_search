import pandas as pd
import json
import csv

player_csv = r"players_21.csv"


def load_attributes():
    """
    :return:
        attribute_list: all attributes for Players to search
        positionen:     all positions of Players
    """
    with open(player_csv, newline='') as f:
        reader = csv.reader(f)
        row1 = next(reader)
    indices = [3, 5, 8, 12, 20, 21] + list(range(24, 60)) + list(range(72, 78))
    attribute_list = [row1[i] for i in indices]
    positionen = [row1[i] for i in range(79, 106)]
    return attribute_list, positionen


def load_data(col=True):
    if col:
        return pd.read_csv(player_csv, low_memory=False)
    else:
        return pd.read_csv(player_csv, low_memory=False, usecols=["Name"])


def search_player(name="", position="", age=99, attribute1="", value1=99, attribute2="", value2=99):
    """
    filters df for all params that aint empty
    :return:
    """
    df = load_data()
    if name != "":
        df = df[df.Name == name]
    if position != "":
        df = df[df.BP == position]
    if age != 99:
        df = df[df.Age == age]
    if attribute1 != "":
        df = df[df[attribute1] >= value1]
    if attribute2 != "":
        df = df[df[attribute2] >= value2]
    return df


def handle_request(json_data):
    """

    :param json_data: json request from search
    :return:
        json that has all infos about filtered players
    """
    req = json.loads(json_data)
    players = search_player(req['name'], req['position'], req['age'], req['attribute1'], req['value1'],
                            req['attribute2'], req['value2'])
    return players.to_json(orient="split")


def get_suggestion(subname):
    series = load_data(False)
    name_suggest = [name for name in series['Name'].to_list() if subname in name]
    return name_suggest


if __name__ == "__main__":
    req_json = '{ "name":"" , "position":"" , "age":30, "attribute1":"POT", "value1":85 ,' \
               '"attribute2":"OVA", "value2":85}'

    print(get_suggestion("Ronal"))
    (attributes, positions) = load_attributes()
    json = handle_request(req_json)
    print(json)
