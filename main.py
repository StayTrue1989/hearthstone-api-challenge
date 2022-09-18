# from multiprocessing import set_start_method
import os

# import hvac
from enum import Enum
from time import perf_counter
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import requests
# from oauthlib.oauth2 import BackendApplicationClient
# from requests_oauthlib import OAuth2Session


from method import card_methods

# Create enum for valid class names that can be used in path parameters
class ClassName(str, Enum):
    """Enum for valid class names that can be used in path parameters"""

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
async def display_card_for_druid_warlock(request: Request):
    """Display cards for druid and warlock classes"""

    t1_start = perf_counter()

    # Start requests session and get access token for Blizzard API calls
    s = card_methods.get_token_session(MY_CLIENT_ID, MY_CLIENT_SECRET)

    card_data = card_methods.get_cards_for_druid_warlock(s)

    card_methods.replace_card_metadata(card_data, s)

    headings = card_methods.create_formatted_headers(card_data)

    data_list = card_methods.format_table_data_for_jinja(card_data)

    # Split the data list to only return the first 10 cards
    data_list = data_list[:10]

    print(f"{len(data_list)} matching cards returned for druid and warlock classes")

    t1_stop = perf_counter()

    print("Elapsed time during call to home path /: ", t1_stop - t1_start)

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
    """Display 10 cards for the class specified in the path parameter"""

    t1_start = perf_counter()

    # Start requests session and get access token for Blizzard API calls
    s = card_methods.get_token_session(MY_CLIENT_ID, MY_CLIENT_SECRET)

    # Get cards for the class specified in the path parameter
    card_data = card_methods.get_cards_from_class(model_name, s)

    card_methods.replace_card_metadata(card_data, s)

    # Create formatted headers for the table
    headings = card_methods.create_formatted_headers(card_data)

    # Format the data for the table to be displayed in the HTML template
    data_list = card_methods.format_table_data_for_jinja(card_data)

    # Split the data list to only return the first 10 cards for the class requested
    data_list = data_list[:10]
    print(f"{len(data_list)} matching cards returned for {model_name} class")

    t1_stop = perf_counter()
    print("Elapsed time during call to path /class/{model_name}: ", t1_stop - t1_start)

    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "headings": headings,
            "data": data_list,
        },
    )


@app.get("/class/{model_name}/all", response_class=HTMLResponse)
async def get_all_cards_for_class(request: Request, model_name: ClassName):
    """Display all cards for the class specified in the path parameter
    Returns all cards for the class passed in the url path parameter."""
    t1_start = perf_counter()

    # Start requests session and get access token for Blizzard API calls
    s = card_methods.get_token_session(MY_CLIENT_ID, MY_CLIENT_SECRET)

    card_data = card_methods.get_cards_from_class(model_name, s)

    card_methods.replace_card_metadata(card_data, s)

    # Create formatted headers for the table
    headings = card_methods.create_formatted_headers(card_data)

    # Format the data for the table to be displayed in the HTML template
    data_list = card_methods.format_table_data_for_jinja(card_data)

    # Prints the number of matching cards returned for the class name passed in the path parameter
    print(f"{len(data_list)} matching cards returned for {model_name} class")

    t1_stop = perf_counter()
    print(
        "Elapsed time during call to path /class/{model_name}/all: ", t1_stop - t1_start
    )

    return templates.TemplateResponse(
        "table.html",
        {
            "request": request,
            "headings": headings,
            "data": data_list,
        },
    )
