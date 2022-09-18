# ** **Note** ** 9-17-2022
### I made some additional changes to the code after submitting it for review. 
### I couldn't help myself. :joy:

Check out the **Releases** page for a copy of the code as it was submitted on 9/13/2022.

You can also compare the **app-enhancements** branch to the release tag **9-13-2022** to see the changes.

# hearthstone-api-challenge

>Create web application to render requested information from the API into a human readable page
>Retrieve details of any 10 cards with the following criteria
>- Class: Druid OR Warlock :white_check_mark: (Capable of retrieving cards with **any** valid class name)
>- Mana: At least 7 :white_check_mark:
>- Rarity: Legendary :white_check_mark:
>
>Display results sorted by card ID in a human readable table that includes:
>- Card image :white_check_mark:
>- Name :white_check_mark:
>- Type :white_check_mark:
>- Rarity :white_check_mark:
>- Set :white_check_mark:
>- Class :white_check_mark:

## Basic Use

You can view the FastAPI swagger docs here:
```
http://127.0.0.1:8000/docs
```
![image](https://user-images.githubusercontent.com/15153542/190015314-ba630d8b-8ae8-44d1-a476-cd7d0953fd2f.png)


The root path shows a mix of 10 cards from the Druid **and** Warlock classes.
```
http://127.0.0.1:8000/
```
![image](https://user-images.githubusercontent.com/15153542/189808343-01110a53-9950-44c2-84b0-d2b968628b71.png)


After re-reading the instructions, I realized it said Druid **OR** Warlock, and not both. Thus, I created the /class path method.



The /class path shows 10 cards from the class you specify in the path parameter (Druid, Warlock, Warrior, Mage, etc)
```
http://127.0.0.1:8000/class/druid
```
![image](https://user-images.githubusercontent.com/15153542/189809088-5eea7596-74b5-446a-8c70-7877080a7990.png)
```
http://127.0.0.1:8000/class/warlock
```
![image](https://user-images.githubusercontent.com/15153542/189808906-3119ae2a-9a07-4027-b349-1530f2b56c52.png)

```
http://127.0.0.1:8000/class/mage
```
![image](https://user-images.githubusercontent.com/15153542/189809184-5079bea4-e20d-4356-820e-81649582e07c.png)


- All the results are sorted by card ID, starting with the smallest at the top. 
- Only cards with a "Legendary" rarity and mana cost of 7 or more are returned. 
- The first 10 cards are returned to the table.


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
1. Provide these credentials locally.
2. Get the credentials from a HashiCorp vault server 


Create a new file named ".env" in the root directory of the project and copy one of the templates below. Save the file when you're finished.

### 1. Configure .env file to load locally provided credentials
Fill in the client id and client secret 
```
# environment variables defined for local development.
# If an environment variable is not found in the .env file,
# load_dotenv will then search for a variable by the given name in the host environment.
MY_CLIENT_ID=<my_client_id>
MY_CLIENT_SECRET=<my_client_secret>

```


### 2. Configure .env file for HachiCorp Vault (Disabled by default)
Fill in the URL of your Vault server and the path to the credentials
```
# Define location of Vault server and path to secret
MY_VAULT_URL="http://localhost:8200"
VAULT_PATH="hs_api_creds"
```

