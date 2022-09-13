import os
import hvac
from enum import Enum
from time import perf_counter
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from method import card_methods

# Create enum for valid class names that can be used in path parameters
class ClassName(str, Enum):
    demonhunter = "demonhunter"
    druid = "druid"
    hunter = "hunter"
    mage = "mage"
    paladin = "paladin"
    priest = "priest"
    rogue = "rogue"
    shaman = "shaman"
    warlock = "warlock"
    warrior = "warrior"
    neutral = "neutral"


load_dotenv()


# .env file boilerplate code to read secret from .env file in local directory
### Not needed if using Vault server ###
MY_CLIENT_ID = os.getenv("MY_CLIENT_ID")
MY_CLIENT_SECRET = os.getenv("MY_CLIENT_SECRET")


# # Set Vault variables to be used in init_server() and read_secret()
# ### Not needed if using .env file to store secrets locally ###
# MY_VAULT_URL = "http://localhost:8200"
# VAULT_PATH = "hs_api_creds"

# Hashicorp Vault boilerplate code to read secret from Vault "Dev" server
# def init_server():

#     client = hvac.Client(url=f"{MY_VAULT_URL}")
#     print(f" Is client authenticated: {client.is_authenticated()}")
#     return client


# def read_secret(client):

#     read_response = client.secrets.kv.v2.read_secret_version(path=f"{VAULT_PATH}")
#     # print(read_response)
#     return read_response


# Initiate server and read secret from Vault server
# client_data = init_server()
# read_data = read_secret(client_data)

# MY_CLIENT_ID = read_data.get("data").get("data").get("MY_CLIENT_ID")
# MY_CLIENT_SECRET = read_data.get("data").get("data").get("MY_CLIENT_SECRET")


# Start of FastAPI code to create web app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_cards_for_druid_warlock(request: Request):

    t1_start = perf_counter()

    # Get cards for Druid and Warlock
    # By default, the get_cards() method will return cards for Druid and Warlock
    # By default, the get_cards() method will return 10 cards
    data = card_methods.get_cards(MY_CLIENT_ID, MY_CLIENT_SECRET)

    (
        set_data,
        class_data,
        type_data,
        rarity_data,
    ) = card_methods.get_all_metadata_variables(MY_CLIENT_ID, MY_CLIENT_SECRET)

    # Replace card metadata with human readable names
    card_methods.replace_card_metadata(
        data, set_data, rarity_data, class_data, type_data
    )

    headings = card_methods.create_formatted_headers(data)

    data_list = card_methods.format_table_data_for_jinja(data)

    t1_stop = perf_counter()

    print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "headings": headings,
            "data": data_list,
        },
    )


@app.get("/class/{model_name}", response_class=HTMLResponse)
async def get_cards_for_class(request: Request, model_name: ClassName):

    t1_start = perf_counter()

    # Get all cards for the class name passed in the url path parameter
    # By default the get_cards_from_class() method will return 10 cards
    data = card_methods.get_cards_from_class(model_name, MY_CLIENT_ID, MY_CLIENT_SECRET)

    (
        set_data,
        class_data,
        type_data,
        rarity_data,
    ) = card_methods.get_all_metadata_variables(MY_CLIENT_ID, MY_CLIENT_SECRET)

    # Replace card metadata with human readable names
    card_methods.replace_card_metadata(
        data, set_data, rarity_data, class_data, type_data
    )

    headings = card_methods.create_formatted_headers(data)

    data_list = card_methods.format_table_data_for_jinja(data)

    t1_stop = perf_counter()

    print("Elapsed time during the whole program in seconds:", t1_stop - t1_start)

    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "headings": headings,
            "data": data_list,
        },
    )
