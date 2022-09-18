"""Module with functions to get data from Blizzard Hearthstone API"""
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# import hvac


def get_token_session(client_id, client_secret):
    """Get token for API call using OAuth2Session and return session object with token"""

    s = requests.Session()

    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    token = oauth.fetch_token(
        token_url="https://us.battle.net/oauth/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    access_token = token.get("access_token")

    s.headers.update({"authorization": f"Bearer {access_token}"})

    return s


def hs_api_call(s):
    """Get all card data for the druid and warlock classes"""
    request_url = "https://us.api.blizzard.com/hearthstone/cards?locale=en_US&manaCost=7%2C8%2C9%2C10&class=warlock,druid&rarity=legendary"

    return s.get(request_url, timeout=5)


def hs_api_call_single(s, class_1):
    """Get all card data for a single class"""
    request_url = f"https://us.api.blizzard.com/hearthstone/cards?locale=en_US&manaCost=7%2C8%2C9%2C10&class={class_1}&rarity=legendary"

    return s.get(request_url, timeout=5)


def filter_cards(card_list):
    """Filter a list of cards to select the fields we want and return a new list of dictionaries"""
    return [
        {
            "id": x["id"],
            "image": x["image"],
            "name": x["name"],
            "cardTypeId": x["cardTypeId"],
            "rarityId": x["rarityId"],
            "cardSetId": x["cardSetId"],
            "classId": x["classId"],
        }
        for x in card_list
    ]


def get_cards_for_druid_warlock(s):

    result = (hs_api_call(s)).json()

    card_list_response = result.get("cards")

    # Filter out just the cards we want from the response and store in a new list
    filtered_card_list = filter_cards(card_list_response)

    # Sort by id in ascending order (lowest to highest)
    return sorted(filtered_card_list, key=lambda d: d["id"])


def get_cards_from_class(class_1, s):
    """Get all cards from a single class and return as a list of dictionaries"""

    result = hs_api_call_single(s, class_1).json()

    card_list_response = result.get("cards")

    # Filter out just the cards we want from the response and store in a new list
    filtered_card_list = filter_cards(card_list_response)

    # Sort by id in ascending order (lowest to highest)
    return sorted(filtered_card_list, key=lambda d: d["id"])


def get_all_metadata(s):
    """Get all metadata from Blizzard Hearthstone API and return as a list of dictionaries"""
    # my_access_token = get_token(MY_CLIENT_ID, MY_CLIENT_SECRET)

    request_url = "https://us.api.blizzard.com/hearthstone/metadata?locale=en_US"
    return s.get(request_url, timeout=5).json()
    # return (requests.get(request_url, timeout=5)).json()


def get_all_metadata_variables(s):
    """Get all metadata for cards and store in variables for later use as dictionaries"""

    all_meta_data = get_all_metadata(s)

    sets_dict = {x["id"]: x["name"] for x in (all_meta_data.get("sets"))}
    # The Legacy set metadata has a unique key and value "aliasSetIds"
    for card_set in all_meta_data.get("sets"):
        if card_set.get("aliasSetIds"):
            for alias in card_set["aliasSetIds"]:
                sets_dict[alias] = card_set["name"]
    classes_dict = {x["id"]: x["name"] for x in (all_meta_data.get("classes"))}
    types_dict = {x["id"]: x["name"] for x in (all_meta_data.get("types"))}
    rarities_dict = {x["id"]: x["name"] for x in (all_meta_data.get("rarities"))}

    return sets_dict, classes_dict, types_dict, rarities_dict


def replace_card_metadata(card_list, s):
    """Replace card metadata with the human readable names from the metadata dictionaries"""

    (
        sets_dict,
        classes_dict,
        types_dict,
        rarities_dict,
    ) = get_all_metadata_variables(s)

    for card in card_list:
        card["cardSetId"] = sets_dict[card["cardSetId"]]
        card["rarityId"] = rarities_dict[card["rarityId"]]
        card["classId"] = classes_dict[card["classId"]]
        card["cardTypeId"] = types_dict[card["cardTypeId"]]
    return card_list


def create_formatted_headers(card_data):
    """Create a list of formatted headers for the card data"""

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
    """Format data for jinja2 template table"""

    # Get values from each card and store in a list of lists
    table_data = [list(card.values()) for card in data]

    for row in table_data:
        # Add card image tag to the image url on each row in table_data
        row[1] = f'<img src="{row[1]}" width="200" >'
        # Remove cardId from each row in table_data (first item in each list)
        row.pop(0)

    return table_data


# Hashicorp Vault boilerplate code to read secret from Vault "Dev" server
# def init_server():

#     client = hvac.Client(url=f"{MY_VAULT_URL}")
#     print(f" Is client authenticated: {client.is_authenticated()}")
#     return client


# def read_secret(client):

#     read_response = client.secrets.kv.v2.read_secret_version(path=f"{VAULT_PATH}")
#     print(read_response)
#     return read_response
