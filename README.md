# hearthstone-api-challenge
hearthstone-api-challenge

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