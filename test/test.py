from getPlayers import search_player, load_attributes, handle_request, get_suggestion


def test_load_attributes():
    attribute, positionen = load_attributes()
    assert type(attribute) == list
    assert type(positionen) == list


def test_search_player():
    df = search_player()
    assert type(df["Name"][0]) == str


def test_handle_request():
    answer = ["Name","Age","OVA","LCB","CB","RCB","RB","GK"]

    req_json = '{ "name":"" , "position":"" , "age":30, "attribute1":"POT", "value1":85 ,' \
               '"attribute2":"OVA", "value2":85}'
    res = handle_request(req_json)
    for item in answer:
        assert item in res


def test_get_suggestion():
    result = ['Cristiano Ronaldo', 'Ronaldinho', 'Ronaldo', 'Ronaldo Esler', 'Ronaldo Cabrais', 'Ronaldo Vieira']
    assert get_suggestion("Ronal") == result
