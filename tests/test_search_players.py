from resources.search_players import SearchPlayers
import pytest
import json


@pytest.mark.parametrize("year", ["15", "16", "17", "18", "19", "20", "21"])
def test_update_dataset(year):
    search = SearchPlayers()
    search.update_dataset(year)
    assert search.year == year
    assert len(search.df.columns) == 106


def test_set_attributes():
    search = SearchPlayers()

    assert search.attributes["info"][1] == "age"
    assert search.attributes["info"][-1] == "physic"
    assert list(search.attributes.keys()) == ["info", "positions", "skills"]


@pytest.mark.parametrize("potential", ["80", "85", "75", ""])
@pytest.mark.parametrize("name", ["Cristiano", "Lewand", "Benzema", "Messi", ""])
def test_get_players(name, potential):
    test_req = {
        "name": name,
        "position": "ST",
        "age": "35",
        "ability1Name": "potential",
        "ability1Value": potential,
        "ability2Name": "overall",
        "ability2Value": "80",
    }

    test_search = SearchPlayers().get_players(test_req)
    assert any(param in test_search for param in [potential, name])


@pytest.mark.parametrize("overall", ["100", "85", "75", ""])
@pytest.mark.parametrize("potential", ["800", "85", "75", "-222"])
@pytest.mark.parametrize("name", ["Cristwiano", "Lewaernd", "Benzerwema", "Mesawesi"])
def test_false_get_players(name, potential, overall):
    test_req = {
        "name": name,
        "position": "ST",
        "age": "35",
        "ability1Name": "potential",
        "ability1Value": potential,
        "ability2Name": "overall",
        "ability2Value": overall,
    }

    test_search = SearchPlayers().get_players(test_req)
    print(test_search)
    assert name not in test_search


@pytest.mark.parametrize("age", ["100", "25", "12", "-12", "35"])
def test_age_get_players(age):
    test_req = {
        "name": "",
        "position": "",
        "age": age,
        "ability1Name": "potential",
        "ability1Value": 80,
        "ability2Name": "overall",
        "ability2Value": "80",
    }

    search_dict = json.loads(SearchPlayers().get_players(test_req))

    if 16 < int(age):
        assert any(search_dict.values())
    else:
        assert not any(search_dict.values())


def test_get_attributes_json():
    search = SearchPlayers()
    assert type(search.get_attributes()) == dict


@pytest.mark.parametrize("name", ["Cristi", "Lewand", "Benzema", "Messi", ""])
def test_get_suggestion(name):
    assert all(
        name in suggested_name
        for suggested_name in SearchPlayers().get_suggestion(name)
    )
