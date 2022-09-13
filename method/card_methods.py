import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import hvac


def get_token(client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(
        token_url="https://us.battle.net/oauth/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    return token.get("access_token")


def hs_api_call(access_token):
    request_url = f"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&manaCost=7%2C8%2C9%2C10&class=warlock,druid&rarity=legendary&access_token={access_token}"
    return requests.get(request_url, timeout=5)


def hs_api_call_single(access_token, class_1):
    request_url = f"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&manaCost=7%2C8%2C9%2C10&class={class_1}&rarity=legendary&access_token={access_token}"
    return requests.get(request_url, timeout=5)


def get_cards(MY_CLIENT_ID, MY_CLIENT_SECRET):

    my_access_token = get_token(MY_CLIENT_ID, MY_CLIENT_SECRET)

    result = (hs_api_call(my_access_token)).json()

    card_list_response = result.get("cards")

    new_list = []
    for x in card_list_response:
        new_dict = {
            "id": x["id"],
            "image": x["image"],
            "name": x["name"],
            "cardTypeId": x["cardTypeId"],
            "rarityId": x["rarityId"],
            "cardSetId": x["cardSetId"],
            "classId": x["classId"],
        }
        new_list.append(new_dict)

    # Sorting list by "id" value from each dict object in the list
    # newlist = sorted(new_list, key=lambda d: d["id"], reverse=True)
    newlist = sorted(new_list, key=lambda d: d["id"])

    # Return the first 10 items in the list
    return newlist[:11]


def get_cards_from_class(class_1, MY_CLIENT_ID, MY_CLIENT_SECRET):

    my_access_token = get_token(MY_CLIENT_ID, MY_CLIENT_SECRET)

    result = hs_api_call_single(my_access_token, class_1)

    jsonResponse = result.json()

    listresponse = jsonResponse.get("cards")

    new_list = []
    for x in listresponse:
        new_dict = {
            "id": x["id"],
            "image": x["image"],
            "name": x["name"],
            "cardTypeId": x["cardTypeId"],
            "rarityId": x["rarityId"],
            "cardSetId": x["cardSetId"],
            "classId": x["classId"],
        }
        new_list.append(new_dict)

    # Sorting list by "id" value from each dict object in the list
    # newlist = sorted(new_list, key=lambda d: d["id"], reverse=True)
    newlist = sorted(new_list, key=lambda d: d["id"])

    # Return the first 10 items in the list
    return newlist[:11]


def get_all_metadata(MY_CLIENT_ID, MY_CLIENT_SECRET):
    """Get all metadata from Blizzard Hearthstone API and return as a list of dictionaries"""
    my_access_token = get_token(MY_CLIENT_ID, MY_CLIENT_SECRET)
    request_url = f"https://us.api.blizzard.com/hearthstone/metadata?locale=en_US&access_token={my_access_token}"
    return (requests.get(request_url, timeout=5)).json()


def replace_card_metadata(card_list, sets, rarities, classes, types):
    for card in card_list:
        for card_set in sets:
            if card["cardSetId"] == card_set["id"]:
                card["cardSetId"] = card_set["name"]
            # Check if card is part of legacy set and if so, replace cardSetId with "Legacy"
            elif (
                card_set.get("aliasSetIds")
                and card["cardSetId"] in card_set["aliasSetIds"]
            ):
                card["cardSetId"] = card_set["name"]
        for rarity in rarities:
            if card["rarityId"] == rarity["id"]:
                card["rarityId"] = rarity["name"]
        for class_ in classes:
            if card["classId"] == class_["id"]:
                card["classId"] = class_["name"]
        for type_ in types:
            if card["cardTypeId"] == type_["id"]:
                card["cardTypeId"] = type_["name"]
    return card_list


def get_all_metadata_variables(MY_CLIENT_ID, MY_CLIENT_SECRET):
    # Get all metadata for cards and store in variables for later use
    all_meta_data = get_all_metadata(MY_CLIENT_ID, MY_CLIENT_SECRET)
    set_data = all_meta_data.get("sets")
    class_data = all_meta_data.get("classes")
    type_data = all_meta_data.get("types")
    rarity_data = all_meta_data.get("rarities")
    return set_data, class_data, type_data, rarity_data


def create_formatted_headers(card_data):
    # Gather header names from first card
    headers = list(card_data[0].keys())

    # Remove cardId from headers
    headers.pop(0)

    # Replace headers with human readable names
    for x in headers:
        if x == "cardSetId":
            headers[headers.index(x)] = "Set"
        elif x == "cardTypeId":
            headers[headers.index(x)] = "Type"
        elif x == "classId":
            headers[headers.index(x)] = "Class"
        elif x == "rarityId":
            headers[headers.index(x)] = "Rarity"
        elif x == "name":
            headers[headers.index(x)] = "Name"
        elif x == "image":
            headers[headers.index(x)] = "Card Image"

    return headers


def format_table_data_for_jinja(data):
    """Format data for jinja2 template"""
    data_list = []
    for x in data:
        data_list.append(list(x.values()))

    for x in data_list:
        x[1] = f'<img src="{x[1]}" width="200" >'
        # Remove cardId from data
        x.pop(0)

    return data_list


# Hashicorp Vault boilerplate code to read secret from Vault "Dev" server
def init_server():

    client = hvac.Client(url=f"{MY_VAULT_URL}")
    print(f" Is client authenticated: {client.is_authenticated()}")
    return client


def read_secret(client):

    read_response = client.secrets.kv.v2.read_secret_version(path=f"{VAULT_PATH}")
    print(read_response)
    return read_response
