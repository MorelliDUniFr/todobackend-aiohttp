# Todo-Backend implemented in Python 3.9 / aiohttp

## Requirements

- Python 3.9.7
- Virtualenv
- MongoDB (installed and running)

## Installation
### Windows
**Creating a virtual environment**
```sh
virtualenv env
```
```sh
env\Scripts\activate
```

**Installing dependencies**
```sh
pip install -r requirements.txt
```

**Populating the database**
```sh
python todobackend/populate_db.py
```

**Running the server**
```sh
python run_server.py
```


### MacOS
**Creating a virtual environment**
```sh
virtualenv env
```
```sh
source env/bin/activate
```

**Installing dependencies**
```sh
pip install -r requirements.txt
```

**Populating the database**
```sh
python3 todobackend/populate_db.py
```

**Running the server**
```sh
python3 run_server.py
```

## Testing the server
Upon successfully launching, you can open up https://todospecs.thing.zone/index.html?http://localhost:8080 in your browser and test against a reference Todo-MVC implementation.



