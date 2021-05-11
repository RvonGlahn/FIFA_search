import pandas as pd
import os
from typing import List, Dict

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

        self.update_dataset(self.year)
        self._set_attributes()

    def update_dataset(self, year: str) -> None:
        """
        Updates year, path and dataframe for provided year.

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
                "pace",
                "shooting",
                "dribbling",
                "passing",
                "defending",
                "physic",
            ],
            "positions": list(map(str.upper, column_names[80:-1])),
            "skills": column_names[39:79],
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
            search_df = search_df[search_df["short_name"].str.contains(req["name"])]

        if req["position"]:
            search_df = search_df[
                search_df["player_positions"].str.contains(req["position"])
            ]

        if req["age"]:
            search_df = search_df[search_df["age"] <= int(req["age"])]

        if req["ability1Name"] and req["ability1Value"]:
            search_df = search_df[
                search_df[req["ability1Name"]] >= int(req["ability1Value"])
            ]

        if req["ability2Name"] and req["ability2Value"]:
            search_df = search_df[
                search_df[req["ability2Name"]] >= int(req["ability2Value"])
            ]

        search_df = search_df.head(20)
        # TODO: Format Players so that they are easier to process
        return search_df.to_json()

    def _build_player_dict(self, df: pd.DataFrame) -> Dict:
        pass

    def get_attributes(self) -> Dict:
        """
        Provides attribute names of dataset as json for info, positions and skills.

        Returns
        -------
        Dict
        """
        return self.attributes

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
        "name": "Neymar",
        "position": "CAM",
        "age": "3",
        "ability1Name": "potential",
        "ability1Value": "80",
        "ability2Name": "overall",
        "ability2Value": "80",
    }

    search = SearchPlayers()
    print(search.get_suggestion("Ronal"))
    json_dat = search.get_players(req_json)
    print(json_dat)
