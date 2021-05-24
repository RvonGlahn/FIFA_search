import pandas as pd
import os
from typing import List, Dict
import json
import re

FILE_PATH = os.path.dirname(__file__)


class SearchPlayers:
    """
    Class that provides functionality to search Players in FIFA from 2015 till today.
    You can search for Player names or individual Attributes that apply to Players.
    Like Potential, Overall, Pace, ...
    """

    def __init__(self):
        """
        Initializes dataframe for year 21.
        """
        self.year = "21"
        self.df = pd.DataFrame()
        self.attributes = {}
        self.grouped_skills = {}

        self.update_dataset(self.year)
        self._set_attributes()

    def update_dataset(self, year: str) -> None:
        """
        Updates year, path and dataframe for provided year. Rename skills.

        Parameters
        ----------
        year : str
            two character string for year (e.g. 21)

        Returns
        -------
        """
        self.year = year
        data_path = os.path.join(FILE_PATH, "data", "players_" + year + ".csv")
        self.df = pd.read_csv(data_path, low_memory=False, encoding="utf-8")
        # self.df = self.df.drop(['player_traits'], axis=1)

        new_skill_names = [
            re.sub(r"^.*?_", "", c) for c in self.df.columns[39:75]
        ] + self.df.columns[75:79].tolist()
        new_columns = (
            self.df.columns[0:39].tolist()
            + new_skill_names
            + self.df.columns[79::].tolist()
        )
        clean_columns = [column.replace("_", " ") for column in new_columns]
        self.df.columns = clean_columns

    def _set_attributes(self):
        """
        Selects relevant attributes(column names) that appear in the dataframe

        Returns
        -------
        """
        # df.dtypes
        column_names = self.df.columns.to_list()

        self.attributes = {
            "info": [
                "short_name",
                "age",
                "club_name",
                "overall",
                "potential",
                "value_eur",
                "wage_eur",
                "player_positions",
                "joined",
                "contract_valid_until",
            ],
            "positions": list(map(str.upper, column_names[80::])),
            "skills": ["overall", "potential"] + column_names[46:79],
        }

        self.grouped_skills = {
            "goalkeeping": column_names[75:80],
            "attacking": column_names[46:51],
            "skill": column_names[51:56],
            "mentality": column_names[66:72],
            "power": column_names[61:66],
            "defending": column_names[72:75],
            "movement": column_names[56:61],
        }

    def get_players(self, req: Dict) -> str:
        """
        Takes search attributes as input and provides df with matching palyers

        Parameters
        ----------
        req: Dict
            dict that contains user request data

        Returns
        -------
        str
        """
        search_df = self.df

        if req["name"]:
            search_df = search_df[search_df["short name"].str.contains(req["name"])]

        if req["position"]:
            search_df = search_df[
                search_df["player positions"].str.contains(req["position"])
            ]

        if req["age"]:
            search_df = search_df[search_df["age"] <= int(req["age"])]

        if req["player value"]:
            search_df = search_df[search_df["value_eur"] <= int(req["player value"])]

        if req["ability1Name"] and req["ability1Value"]:
            search_df = search_df[
                search_df[req["ability1Name"]] >= int(req["ability1Value"])
            ]

        if req["ability2Name"] and req["ability2Value"]:
            search_df = search_df[
                search_df[req["ability2Name"]] >= int(req["ability2Value"])
            ]

        search_df = search_df.head(20).fillna(0)

        player_list = self._build_player_dict(search_df)
        return json.dumps(player_list)

    def _build_player_dict(self, df: pd.DataFrame) -> List:
        """
        Build dictionary with dict format that can be easily handled by frontend

        Parameters
        ----------
        df : pd.DataFrame
            dataframe with search results

        Returns
        -------
        List
        """
        players = []
        position_list = list(self.df.columns.to_list()[79::])
        skill_list = self.attributes["skills"].copy()

        for (index_label, player) in df.iterrows():
            player_dict = {
                "info": player[self.attributes["info"]].to_dict(),
                "positions": player[position_list].to_dict(),
                "skills": player[skill_list].to_dict(),
            }
            dict_keys = player_dict["skills"].copy()
            for key in dict_keys.keys():
                # filter skills lower than 40
                try:
                    if int(player_dict["skills"][key]) < 45:
                        player_dict["skills"].pop(key)
                        continue
                except ValueError:
                    player_dict["skills"].pop(key)

            players.append(player_dict)

        return players

    def get_attributes(self) -> Dict:
        """
        Provides attribute names of dataset as json for info, positions and skills.

        Returns
        -------
        Dict
        """
        attributes = self.attributes.copy()
        attributes["skills"] = sorted(attributes["skills"])
        return attributes

    def get_grouped_attributes(self) -> Dict:
        """
        Provides attribute names of dataset as json for info, positions and skills.

        Returns
        -------
        Dict
        """
        return self.grouped_skills

    def get_suggestion(self, subname: str) -> List[str]:
        """
        Provides suggestion for player names in dataset
        Parameters
        ----------
        subname : str
            part of name that gets checked for suggestion

        Returns
        -------
        List[str]
        """
        name_suggest = [
            name for name in self.df["short_name"].to_list() if subname in name
        ]
        return name_suggest


if __name__ == "__main__":  # pragma: no cover
    req_json = {
        "name": "",
        "position": "CAM",
        "age": "30",
        "ability1Name": "potential",
        "ability1Value": "80",
        "ability2Name": "overall",
        "ability2Value": "80",
        "player_value": "99999999999",
    }

    search = SearchPlayers()
    search.get_attributes()
    print(search.get_suggestion("Ronal"))
    json_dat = search.get_players(req_json)
    print(json_dat)
