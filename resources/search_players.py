import pandas as pd
import json
import os

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

        self._set_attributes()
        self.update_dataset(self.year)

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
                "player_positons",
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

    def get_players(self, json_data: str) -> str:
        """
        Takes search attributes as input and provides df with matching palyers

        Parameters
        ----------
        json_data: str
            json string that contains user request data

        Returns
        -------
        pd.DataFrame
        """
        req = json.loads(json_data)

        search_df = self.df

        if req["name"]:
            search_df = search_df[search_df["name"].str.contains(req["name"])]

        if req["position"]:
            search_df = search_df[search_df["player_positons"] == req["position"]]

        if req["age"]:
            search_df = search_df[search_df.age >= req["age"]]

        if req["ability1name"]:
            search_df = search_df[
                search_df[req["ability1name"]] >= int(req["ability1Value"])
            ]

        if req["ability2Name"]:
            search_df = search_df[
                search_df[req["ability2Name"]] >= int(req["ability2Value"])
            ]

        return search_df.to_json()

    def get_attributes_json(self) -> str:
        """
        Provides attribute names of dataset as json for info, positions and skills.

        Returns
        -------
        str
        """
        return json.dumps(self.attributes)

    def get_suggestion(self, subname):
        name_suggest = [name for name in self.df["Name"].to_list() if subname in name]
        return name_suggest


if __name__ == "__main__":
    req_json = (
        '{ "name":"" , "position":"" , "age":30, "ability1Name":"POT", "ability1Value":80 , '
        '"ability2Name":"OVA", "ability2Value":80}'
    )

    search = SearchPlayers()
    print(search.get_suggestion("Ronal"))
    json_dat = search.get_players(req_json)
    print(json_dat)
