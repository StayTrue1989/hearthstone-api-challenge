# hearthstone-api-challenge

## Basic Use

The root path shows a mix of 10 cards from the Druid and Warlock classes.
```
http://127.0.0.1:8000/
```

The /class path shows 10 cards from the class you specify in the path parameter
```
http://127.0.0.1:8000/class/mage
```
```
http://127.0.0.1:8000/class/warrior
```

All the results are sorted by card ID, starting with the smallest at the top. The first 10 cards are returned to the table.


## Setup the API project locally

To create a virtual environment, go to the project’s directory and run venv.
```
py -m venv env
```
venv will create a virtual Python installation in the env folder.

Activate the virtual environment
```
.\env\Scripts\activate
```

Install required packages from requirements.txt file
```
py -m pip install -r requirements.txt
```

> ### Before running the next command, look [below](https://github.com/StayTrue1989/hearthstone-api-challenge/edit/main/README.md#provide-the-required-client-id-and-client-secret-necessary-to-authenticate-with-the-blizzard-hearthstone-api) for instructions to configure credentails for API authentication.

Run the FastAPI project
```
uvicorn main:app --reload
```


## Provide the required "client id" and "client secret" necessary to authenticate with the Blizzard Hearthstone API
There are two methods we can use to provide these credentails
1. Get the credentials from a HashiCorp vault server
2. Provide these credentials locally.

Create a new file called ".env" in the root directory of the project and copy one of the templates below.
### Configure .env file for HachiCorp Vault
Fill in the URL of your Vault server and the path to the credentials
```
# Define location of Vault server and path to secret
MY_VAULT_URL="http://localhost:8200"
VAULT_PATH="hs_api_creds"
```


### Configure .env file to store MY_CLIENT_ID and MY_CLIENT_SECRET locally
Fill in the client id and client secret 
```
# environment variables defined for local development.
# If an environment variable is not found in the .env file,
# load_dotenv will then search for a variable by the given name in the host environment.
MY_CLIENT_ID=<my_client_id>
MY_CLIENT_SECRET=<my_client_secret>

```
