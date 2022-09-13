# hearthstone-api-challenge

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

Run the FastAPI project
```
uvicorn main:app --reload
```

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

All the results are sorted by card ID, in reverse. The first 10 cards are returned to the table