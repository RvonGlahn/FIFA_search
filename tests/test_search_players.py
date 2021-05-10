from resources.search_players import SearchPlayers
import pytest


@pytest.mark.parametrize("year", ["15", "16", "17", "18", "19", "20", "21"])
def test_update_dataset(year):
    search = SearchPlayers()
    search.update_dataset(year)
    assert search.year == year
    assert len(search.df.columns) == 106


def test_set_attributes():
    pass


def test_get_players():
    pass


def test_get_attributes_json():
    pass


def test_get_suggestion():
    pass
